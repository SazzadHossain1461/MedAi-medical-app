import numpy as np
from collections import deque
import random
import logging
from tensorflow import keras

logger = logging.getLogger(__name__)

class RLConfig:
    """Reinforcement Learning Configuration"""
    LEARNING_RATE = 0.01
    GAMMA = 0.95
    EPSILON_DECAY = 0.995
    EPSILON_MIN = 0.01
    MEMORY_SIZE = 2000
    BATCH_SIZE = 32
    EPISODES = 1000

class PredictionEnvironment:
    """Custom environment for RL optimization of medical predictions"""
    
    def __init__(self, model, scaler, X_data, y_data, disease_type):
        self.model = model
        self.scaler = scaler
        self.X_data = X_data
        self.y_data = y_data
        self.disease_type = disease_type
        self.current_step = 0
        self.max_steps = len(X_data)
        self.action_space_size = 10  # More granular threshold control
        
    def reset(self):
        """Reset environment"""
        self.current_step = 0
        return self.get_state()
    
    def get_state(self):
        """Get current state (scaled features)"""
        if self.current_step >= len(self.X_data):
            self.current_step = 0
        
        # Scale the input data like in API
        state = self.X_data[self.current_step].reshape(1, -1)
        scaled_state = self.scaler.transform(state)
        return scaled_state[0]
    
    def step(self, action):
        """Execute action and return reward"""
        if self.current_step >= len(self.X_data):
            self.current_step = 0
            
        state = self.X_data[self.current_step].reshape(1, -1)
        true_label = self.y_data[self.current_step]
        
        # Scale input like in API
        scaled_state = self.scaler.transform(state)
        
        # Get prediction (handles both binary and multi-class like API)
        prediction = self.model.predict(scaled_state, verbose=0)[0]
        
        # Convert threshold action to probability threshold (0.1 to 1.0)
        threshold = (action + 1) / 10.0
        
        # Handle different prediction formats like API - FIXED SYNTAX ERROR HERE
        if len(prediction) == 1:
            # Binary classification with single output
            prediction_prob = float(prediction[0])
            predicted_label = 1 if prediction_prob >= threshold else 0
            correct = predicted_label == true_label
        else:
            # Multi-class classification
            prediction_prob = float(np.max(prediction))
            predicted_label = np.argmax(prediction)
            # For multi-class, we need to adjust reward calculation
            if true_label > 1:  # If true label is also multi-class
                correct = predicted_label == true_label
            else:
                # Handle binary true labels with multi-class predictions
                correct = (predicted_label == 1) == (true_label == 1)
        
        # Enhanced reward system
        if correct:
            # Higher reward for correct predictions with appropriate confidence
            confidence_reward = min(prediction_prob, 1.0) if predicted_label == 1 else min(1 - prediction_prob, 1.0)
            reward = 1.0 + confidence_reward
        else:
            # Penalize incorrect predictions, more penalty for high confidence wrong predictions
            confidence_penalty = min(prediction_prob, 1.0) if predicted_label == 1 else min(1 - prediction_prob, 1.0)
            reward = -2.0 - confidence_penalty
        
        self.current_step += 1
        done = self.current_step >= self.max_steps
        
        next_state = self.get_state() if not done else np.zeros_like(self.get_state())
        
        logger.debug(f"Step {self.current_step}: Action={action}, Threshold={threshold:.2f}, "
                    f"Predicted={predicted_label}, Actual={true_label}, Reward={reward:.2f}")
        
        return next_state, reward, done, {
            'prediction_prob': prediction_prob,
            'threshold': threshold,
            'correct': correct
        }
    
    def render(self):
        """Render environment state"""
        pass


class QLearningAgent:
    """Q-Learning Agent for optimizing prediction thresholds"""
    
    def __init__(self, state_size, action_size, learning_rate=0.01, gamma=0.95):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.gamma = gamma
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
        self.epsilon_min = 0.01
        self.memory = deque(maxlen=RLConfig.MEMORY_SIZE)
        
        # Simple Q-table (in practice, you'd use function approximation for large state spaces)
        self.q_table = {}
        
        logger.info(f"QLearningAgent initialized with state_size={state_size}, action_size={action_size}")
        
    def get_state_key(self, state):
        """Convert state to hashable key for Q-table"""
        # Discretize state for Q-table (simplified approach)
        return tuple(np.round(state, 1))
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Select action using epsilon-greedy policy"""
        state_key = self.get_state_key(state)
        
        if np.random.random() <= self.epsilon:
            return random.randint(0, self.action_size - 1)
        
        # Initialize Q-values if state not seen
        if state_key not in self.q_table:
            self.q_table[state_key] = np.zeros(self.action_size)
        
        return np.argmax(self.q_table[state_key])
    
    def replay(self, batch_size=32):
        """Train on batch of experiences"""
        if len(self.memory) < batch_size:
            return
        
        batch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in batch:
            state_key = self.get_state_key(state)
            next_state_key = self.get_state_key(next_state)
            
            # Initialize Q-values if states not seen
            if state_key not in self.q_table:
                self.q_table[state_key] = np.zeros(self.action_size)
            if next_state_key not in self.q_table:
                self.q_table[next_state_key] = np.zeros(self.action_size)
            
            # Q-learning update
            current_q = self.q_table[state_key][action]
            if done:
                target = reward
            else:
                target = reward + self.gamma * np.max(self.q_table[next_state_key])
            
            self.q_table[state_key][action] = current_q + self.learning_rate * (target - current_q)
        
        # Decay epsilon
        self.decay_epsilon()
    
    def decay_epsilon(self):
        """Decay exploration rate"""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


class DQNAgent:
    """Deep Q-Network Agent for more complex state spaces"""
    
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=RLConfig.MEMORY_SIZE)
        self.gamma = RLConfig.GAMMA
        self.epsilon = RLConfig.EPSILON_MIN
        self.epsilon_min = RLConfig.EPSILON_MIN
        self.epsilon_decay = RLConfig.EPSILON_DECAY
        self.learning_rate = RLConfig.LEARNING_RATE
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()
        
        logger.info(f"DQNAgent initialized with state_size={state_size}, action_size={action_size}")
    
    def _build_model(self):
        """Build neural network for Q-function approximation"""
        model = keras.Sequential([
            keras.layers.Dense(24, input_dim=self.state_size, activation='relu'),
            keras.layers.Dense(24, activation='relu'),
            keras.layers.Dense(self.action_size, activation='linear')
        ])
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=self.learning_rate))
        return model
    
    def update_target_model(self):
        """Update target model weights"""
        self.target_model.set_weights(self.model.get_weights())
    
    def remember(self, state, action, reward, next_state, done):
        """Store experience in memory"""
        self.memory.append((state, action, reward, next_state, done))
    
    def act(self, state):
        """Select action using epsilon-greedy policy"""
        if np.random.random() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state.reshape(1, -1), verbose=0)
        return np.argmax(act_values[0])
    
    def replay(self, batch_size=32):
        """Train on batch of experiences"""
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state.reshape(1, -1), verbose=0)
            if done:
                target[0][action] = reward
            else:
                t = self.target_model.predict(next_state.reshape(1, -1), verbose=0)
                target[0][action] = reward + self.gamma * np.amax(t[0])
            
            self.model.fit(state.reshape(1, -1), target, epochs=1, verbose=0)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


def train_rl_agent(models, scalers, X_train, y_train, disease_type):
    """Train RL agent for a specific disease model"""
    try:
        if disease_type not in models or models[disease_type] is None:
            logger.error(f"Model for {disease_type} not available")
            return None
        
        # Create environment
        env = PredictionEnvironment(
            model=models[disease_type],
            scaler=scalers[disease_type],
            X_data=X_train,
            y_data=y_train,
            disease_type=disease_type
        )
        
        state_size = X_train.shape[1]
        action_size = env.action_space_size
        
        # Choose agent type based on state size
        if state_size <= 20:  # Small state space
            agent = QLearningAgent(state_size, action_size)
        else:  # Larger state space
            agent = DQNAgent(state_size, action_size)
        
        # Training loop
        best_avg_reward = -float('inf')
        for episode in range(RLConfig.EPISODES):
            state = env.reset()
            total_reward = 0
            steps = 0
            
            while True:
                action = agent.act(state)
                next_state, reward, done, info = env.step(action)
                agent.remember(state, action, reward, next_state, done)
                
                state = next_state
                total_reward += reward
                steps += 1
                
                if done or steps >= env.max_steps:
                    break
            
            # Experience replay
            agent.replay(RLConfig.BATCH_SIZE)
            
            avg_reward = total_reward / steps if steps > 0 else 0
            if episode % 100 == 0:
                logger.info(f"Episode {episode}, Average Reward: {avg_reward:.2f}, Epsilon: {agent.epsilon:.3f}")
            
            if avg_reward > best_avg_reward:
                best_avg_reward = avg_reward
        
        logger.info(f"RL training completed for {disease_type}. Best avg reward: {best_avg_reward:.2f}")
        return agent
        
    except Exception as e:
        logger.error(f"Error training RL agent for {disease_type}: {str(e)}")
        return None


def optimize_threshold_with_rl(agent, state):
    """Use trained RL agent to optimize prediction threshold"""
    if agent is None:
        return 0.5  # Default threshold
    
    action = agent.act(state)
    optimized_threshold = (action + 1) / 10.0  # Convert to 0.1-1.0 range
    return optimized_threshold