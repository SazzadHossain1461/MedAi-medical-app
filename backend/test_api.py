"""
Test script for API endpoints
"""

import requests
import json
import time
import random

BASE_URL = 'http://localhost:5000'

class APITester:
    """Test API endpoints"""
    
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_health_check(self):
        """Test health check endpoint"""
        print("\n" + "="*60)
        print("Testing Health Check Endpoint")
        print("="*60)
        
        try:
            response = self.session.get(f'{self.base_url}/api/health')
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_model_info(self):
        """Test model info endpoint"""
        print("\n" + "="*60)
        print("Testing Model Info Endpoint")
        print("="*60)
        
        try:
            response = self.session.get(f'{self.base_url}/api/model-info')
            print(f"Status Code: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_dengue_prediction(self):
        """Test dengue prediction endpoint with correct features"""
        print("\n" + "="*60)
        print("Testing Dengue Prediction Endpoint")
        print("="*60)
        
        # Using the exact 13 features expected by the API
        test_data = {
            'Age': 35,
            'Gender': 1,
            'NS1': 1,
            'IgG': 0,
            'IgM': 1,
            'Area': 2,
            'AreaType': 1,
            'HouseType': 2,
            'District_encoded': 5,
            'Temperature': 39.5,
            'Symptoms': 1,
            'Platelet_Count': 120000,
            'WBC_Count': 5000
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/dengue/predict',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_dengue_batch_predict(self):
        """Test dengue batch prediction endpoint"""
        print("\n" + "="*60)
        print("Testing Dengue Batch Prediction Endpoint")
        print("="*60)
        
        batch_data = [
            {
                'Age': 25,
                'Gender': 0,
                'NS1': 0,
                'IgG': 1,
                'IgM': 0,
                'Area': 1,
                'AreaType': 2,
                'HouseType': 1,
                'District_encoded': 3,
                'Temperature': 38.2,
                'Symptoms': 1,
                'Platelet_Count': 150000,
                'WBC_Count': 6000
            },
            {
                'Age': 45,
                'Gender': 1,
                'NS1': 1,
                'IgG': 0,
                'IgM': 1,
                'Area': 3,
                'AreaType': 1,
                'HouseType': 2,
                'District_encoded': 7,
                'Temperature': 40.1,
                'Symptoms': 1,
                'Platelet_Count': 80000,
                'WBC_Count': 3500
            }
        ]
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/dengue/batch-predict',
                json=batch_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_dengue_risk_assessment(self):
        """Test dengue risk assessment endpoint"""
        print("\n" + "="*60)
        print("Testing Dengue Risk Assessment Endpoint")
        print("="*60)
        
        test_data = {
            'Age': 35,
            'Gender': 1,
            'NS1': 1,
            'IgG': 0,
            'IgM': 1,
            'Area': 2,
            'AreaType': 1,
            'HouseType': 2,
            'District_encoded': 5,
            'Temperature': 39.5,
            'Symptoms': 1,
            'Platelet_Count': 120000,
            'WBC_Count': 5000
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/dengue/risk-assessment',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_kidney_prediction(self):
        """Test kidney disease prediction endpoint with correct features"""
        print("\n" + "="*60)
        print("Testing Kidney Disease Prediction Endpoint")
        print("="*60)
        
        # Using the exact 13 features expected by the API
        test_data = {
            'age': 45,
            'bp': 140,
            'sg': 1.02,
            'al': 1,
            'su': 0,
            'bgr': 120,
            'bu': 25,
            'sc': 1.2,
            'sod': 138,
            'pot': 5.2,
            'hemo': 10.5,
            'pcv': 35,
            'wc': 8000
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/kidney/predict',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_kidney_risk_assessment(self):
        """Test kidney risk assessment endpoint"""
        print("\n" + "="*60)
        print("Testing Kidney Risk Assessment Endpoint")
        print("="*60)
        
        test_data = {
            'age': 45,
            'bp': 140,
            'sg': 1.02,
            'al': 1,
            'su': 0,
            'bgr': 120,
            'bu': 25,
            'sc': 1.2,
            'sod': 138,
            'pot': 5.2,
            'hemo': 10.5,
            'pcv': 35,
            'wc': 8000
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/kidney/risk-assessment',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_mental_health_assessment(self):
        """Test mental health assessment endpoint with correct features"""
        print("\n" + "="*60)
        print("Testing Mental Health Assessment Endpoint")
        print("="*60)
        
        # Using the exact 13 features expected by the API
        test_data = {
            'age': 30,
            'gender': 1,
            'employment': 2,
            'work_env': 3,
            'stress': 7,
            'sleep': 5,
            'activity': 2,
            'depression': 6,
            'anxiety': 7,
            'support': 3,
            'productivity': 4,
            'mh_history': 1,
            'treatment': 0
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/mental-health/assessment',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_mental_health_therapy_plan(self):
        """Test mental health therapy plan endpoint"""
        print("\n" + "="*60)
        print("Testing Mental Health Therapy Plan Endpoint")
        print("="*60)
        
        test_data = {
            'age': 30,
            'gender': 1,
            'employment': 2,
            'work_env': 3,
            'stress': 7,
            'sleep': 5,
            'activity': 2,
            'depression': 6,
            'anxiety': 7,
            'support': 3,
            'productivity': 4,
            'mh_history': 1,
            'treatment': 0
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/mental-health/therapy-plan',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_mental_health_chat(self):
        """Test mental health chat endpoint"""
        print("\n" + "="*60)
        print("Testing Mental Health Chat Endpoint")
        print("="*60)
        
        test_data = {
            'message': 'I have been feeling very stressed and anxious lately',
            'user_id': 'test_user_123'
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/api/mental-health/chat',
                json=test_data,
                headers={'Content-Type': 'application/json'}
            )
            print(f"Status Code: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {json.dumps(response.json(), indent=2)}")
            else:
                print(f"Error Response: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
    
    def test_model_evaluation(self):
        """Test model evaluation endpoints"""
        print("\n" + "="*60)
        print("Testing Model Evaluation Endpoints")
        print("="*60)
        
        diseases = ['dengue', 'kidney', 'mental_health']
        results = []
        
        for disease in diseases:
            try:
                print(f"\nTesting {disease} evaluation...")
                response = self.session.post(
                    f'{self.base_url}/api/{disease}/evaluate',
                    json={},  # Empty data for demo
                    headers={'Content-Type': 'application/json'}
                )
                print(f"Status Code for {disease}: {response.status_code}")
                if response.status_code == 200:
                    print(f"{disease} evaluation successful")
                    results.append(True)
                else:
                    print(f"{disease} evaluation failed: {response.text}")
                    results.append(False)
            except Exception as e:
                print(f"Error testing {disease} evaluation: {str(e)}")
                results.append(False)
        
        return all(results)
    
    def test_batch_evaluation(self):
        """Test batch evaluation endpoints"""
        print("\n" + "="*60)
        print("Testing Batch Evaluation Endpoints")
        print("="*60)
        
        test_predictions = {
            'predictions': [
                {'prediction': 1, 'probability': 0.85, 'status': 'success'},
                {'prediction': 0, 'probability': 0.25, 'status': 'success'},
                {'prediction': 1, 'probability': 0.72, 'status': 'success'}
            ]
        }
        
        diseases = ['dengue', 'kidney', 'mental_health']
        results = []
        
        for disease in diseases:
            try:
                print(f"\nTesting {disease} batch evaluation...")
                response = self.session.post(
                    f'{self.base_url}/api/{disease}/batch-evaluate',
                    json=test_predictions,
                    headers={'Content-Type': 'application/json'}
                )
                print(f"Status Code for {disease}: {response.status_code}")
                if response.status_code == 200:
                    print(f"{disease} batch evaluation successful")
                    results.append(True)
                else:
                    print(f"{disease} batch evaluation failed: {response.text}")
                    results.append(False)
            except Exception as e:
                print(f"Error testing {disease} batch evaluation: {str(e)}")
                results.append(False)
        
        return all(results)
    
    def run_all_tests(self):
        """Run all tests"""
        print("\n" + "="*70)
        print("STARTING API TEST SUITE")
        print("="*70)
        
        results = {
            'health_check': self.test_health_check(),
            'model_info': self.test_model_info(),
            'dengue_prediction': self.test_dengue_prediction(),
            'dengue_batch_prediction': self.test_dengue_batch_predict(),
            'dengue_risk_assessment': self.test_dengue_risk_assessment(),
            'kidney_prediction': self.test_kidney_prediction(),
            'kidney_risk_assessment': self.test_kidney_risk_assessment(),
            'mental_health_assessment': self.test_mental_health_assessment(),
            'mental_health_therapy_plan': self.test_mental_health_therapy_plan(),
            'mental_health_chat': self.test_mental_health_chat(),
            'model_evaluation': self.test_model_evaluation(),
            'batch_evaluation': self.test_batch_evaluation(),
        }
        
        print("\n" + "="*70)
        print("TEST RESULTS SUMMARY")
        print("="*70)
        
        for test_name, result in results.items():
            status = "✓ PASSED" if result else "✗ FAILED"
            print(f"{test_name:<30}: {status}")
        
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        print(f"\nTotal: {passed}/{total} tests passed")
        print("="*70 + "\n")
        
        return results


def wait_for_server(max_attempts=10, delay=2):
    """Wait for the server to be ready"""
    print("Waiting for API server to be ready...")
    
    for attempt in range(max_attempts):
        try:
            response = requests.get(f'{BASE_URL}/api/health', timeout=5)
            if response.status_code == 200:
                print("✓ Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        if attempt < max_attempts - 1:
            print(f"Attempt {attempt + 1}/{max_attempts} - Server not ready, waiting {delay} seconds...")
            time.sleep(delay)
    
    print("✗ Server did not become ready in time")
    return False


def main():
    """Main test runner"""
    
    if not wait_for_server():
        print("Cannot run tests - server is not available")
        exit(1)
    
    tester = APITester()
    results = tester.run_all_tests()
    
    # Exit with appropriate code
    if all(results.values()):
        print("✓ All tests passed!")
        exit(0)
    else:
        print("✗ Some tests failed")
        exit(1)


if __name__ == '__main__':
    main()