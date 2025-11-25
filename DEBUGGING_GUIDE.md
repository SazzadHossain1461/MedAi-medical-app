# Debugging & Troubleshooting Guide

## ❌ Common Issues & Solutions

### Issue 1: "Prediction failed" Error

**Symptoms**:
- Click "Get Prediction" button
- See error toast: "Prediction failed. Please check your inputs."
- Nothing happens

**Solutions**:

**Step 1**: Check Backend is Running
```bash
# Terminal 1 - Backend
cd backend
python main.py api

# Should see: "Running on http://0.0.0.0:5000"
```

**Step 2**: Check Frontend Console Logs
```
Press F12 → Console tab
Look for errors like:
- "TypeError: Cannot read property 'probability'"
- "Network error"
- "401 Unauthorized"
```

**Step 3**: Verify API Endpoint
```bash
# Test API manually
curl -X GET http://localhost:5000/api/health

# Should respond: {"status": "healthy"}
```

**Step 4**: Check Network Tab
```
Press F12 → Network tab
Click "Get Prediction"
Look for POST request to /api/dengue/predict
- Green status = 200 (Good)
- Red status = Error (Check response)
```

---

### Issue 2: Data Type Errors

**Symptoms**:
- Error: "TypeError: 'str' object cannot be interpreted as an integer"
- Error: "Invalid input types"

**Root Cause**: Form data not converted to numbers

**Fix**: Already implemented in updated code
```javascript
// This is already done:
const numericFormData = {
  Age: parseFloat(formData.Age),
  Temperature: parseFloat(formData.Temperature),
  // ... etc
};
```

**To Verify**:
1. Open DevTools Console
2. Look for "Sending data:" log
3. Check all values are numbers, not strings
```
Example Output:
Sending data: {
  Age: 30,           ✓ number
  Temperature: 37.5  ✓ number
  Platelet_Count: 150000  ✓ number
}
```

---

### Issue 3: "Missing Feature" Warnings

**Symptoms**:
- See warnings in console
- Still get prediction but accuracy may be low

**Example**:
```
WARNING - Missing feature Age in input, using default value 0.0
WARNING - Missing feature Temperature in input, using default value 0.0
```

**Solution**:
- Fill ALL required fields (marked with *)
- Make sure dropdown values are selected
- Don't leave any field empty

---

### Issue 4: Same Result Every Time

**Symptoms**:
- Make prediction with different values
- Get same result twice

**Root Cause**: Fixed in updated code
- Was: Result state not clearing
- Now: `setResult(null)` clears before each prediction

**Verify Fix**:
1. Make first prediction → Note the score
2. Change form values completely
3. Make second prediction → Should show DIFFERENT score
4. Go to History → Should show BOTH predictions

---

### Issue 5: API Timeout

**Symptoms**:
- Prediction button keeps showing "Analyzing..."
- After 30 seconds: Error

**Solutions**:

**Check 1**: Is Backend Running?
```bash
# Should see this running
python main.py api
```

**Check 2**: Is it Processing?
```
Look at backend terminal for logs like:
- "Starting training pipeline for DENGUE"
- "Database initialized successfully"
- "Models loaded successfully"
```

**Check 3**: Are Models Trained?
```bash
# Check if model files exist:
backend/models/dengue_model.h5
backend/models/kidney_model.h5
backend/models/mental_health_model.h5

# If missing, train models:
python main.py train-all
```

---

### Issue 6: CORS Error

**Symptom**:
```
Error: Access to XMLHttpRequest blocked by CORS policy
```

**Fix**: Already configured in backend
```python
# In api_endpoints.py:
from flask_cors import CORS
CORS(app)  # Already done
```

**If Still Occurs**:
1. Restart backend: `python main.py api`
2. Clear browser cache: Ctrl+Shift+Delete
3. Try in incognito window

---

## 🔧 Quick Fix Checklist

Before debugging, run through this checklist:

```
[ ] Backend is running: python main.py api
[ ] Frontend is running: npm start
[ ] Browser shows: http://localhost:3000
[ ] You're logged in (see username in navbar)
[ ] All required fields have values (*)
[ ] Dropdown fields have selections (not blank)
[ ] No console errors shown (F12)
[ ] API health check passes:
    - Go to http://localhost:5000/api/health
    - See: {"status": "healthy"}
[ ] Browser console shows "Sending data:" logs
```

---

## 📋 Manual Testing

### Test 1: Complete Dengue Prediction

**Steps**:
1. Login: demo@medai.com / demo123
2. Go to Dengue Prediction
3. Fill form:
   - Age: 30
   - Gender: Male
   - Temperature: 38.5
   - Platelet Count: 120000
   - NS1: Positive
   - WBC Count: 5000
   - All others: any values
4. Click "Get Prediction"
5. Should see result in 1-2 seconds
6. Try again with different Temperature: 37.0
7. Should show DIFFERENT result
8. Go to History
9. Should see BOTH predictions

**Expected Result**:
- First prediction: Higher temperature → Higher risk
- Second prediction: Lower temperature → Lower risk

---

### Test 2: Complete Kidney Disease Prediction

**Steps**:
1. Go to Kidney Disease
2. Fill form:
   - Age: 55
   - BP: 160
   - Serum Creatinine: 2.5
   - All others: pre-filled values
3. Click "Get Prediction"
4. Should see:
   - Risk level (High/Medium/Low)
   - CKD Stage
   - Confidence %
5. Try with low Serum Creatinine: 0.8
6. Should show LOW risk

---

### Test 3: History Tracking

**Steps**:
1. Make 3-4 predictions (dengue, kidney, mental health)
2. Go to History
3. Should see ALL predictions with:
   - Disease type
   - Risk level
   - Confidence score
   - Timestamp
4. Filter by disease type
5. Should filter correctly
6. Sort by risk level
7. Should reorder
8. Download data
9. Should download JSON file
10. Delete a prediction
11. Should disappear from history

---

## 🎯 Backend Logs - What to Look For

### Good Signs:
```
✓ "Database initialized successfully"
✓ "Models loaded successfully"
✓ "Server starting on 0.0.0.0:5000"
✓ "POST /api/dengue/predict HTTP/1.1" 200
✓ "Dengue prediction made: High Risk"
```

### Bad Signs:
```
✗ "Model for dengue not available"
✗ "Error training dengue model"
✗ "TypeError: 'str' object is not callable"
✗ "POST /api/dengue/predict HTTP/1.1" 500
```

---

## 🐛 Advanced Debugging

### Enable Request Logging

**In frontend/src/api/api.js**, uncomment logs:
```javascript
axiosInstance.interceptors.request.use(
  (config) => {
    console.log('Request:', config.method, config.url, config.data);
    return config;
  }
);

axiosInstance.interceptors.response.use(
  (response) => {
    console.log('Response:', response.data);
    return response;
  }
);
```

### Check Browser Storage

**In Console Tab**:
```javascript
// See saved predictions
localStorage.getItem('predictionHistory_YOUR_USER_ID')

// See user data
localStorage.getItem('user')

// See all storage
localStorage
```

### Check Network Request/Response

1. Open DevTools (F12)
2. Go to Network tab
3. Make prediction
4. Click on the POST request to /api/dengue/predict
5. Check:
   - **Request Headers**: Content-Type should be application/json
   - **Request Payload**: Should show numeric values
   - **Response**: Should show prediction result
   - **Status**: Should be 200 (green)

---

## 📞 Error Messages & Meanings

| Error | Cause | Fix |
|-------|-------|-----|
| "Prediction failed" | API error or data type issue | Check console logs, verify numeric conversion |
| "Missing required field" | Form validation failed | Fill all * marked fields |
| "Network error" | Backend not running | Start backend: `python main.py api` |
| "TypeError: str is not callable" | String passed instead of number | Already fixed in updated code |
| "Model not available" | Models not trained | Run: `python main.py train-all` |
| "CORS error" | Browser blocking request | Restart backend, check CORS enabled |
| "401 Unauthorized" | Auth issue | Re-login with demo account |
| "Database error" | DB not initialized | Restart backend |

---

## ✅ Final Verification

Run this quick test:

```javascript
// In Browser Console:

// 1. Check authentication
console.log(JSON.parse(localStorage.getItem('user')));
// Should show: {id: "xxx", email: "demo@medai.com", ...}

// 2. Check API
fetch('http://localhost:5000/api/health')
  .then(r => r.json())
  .then(d => console.log('API Status:', d.status))
// Should show: "API Status: healthy"

// 3. Make test prediction
const testData = {
  Age: 30, Gender: 1, NS1: 0, IgG: 0, IgM: 0,
  Area: 1, AreaType: 1, HouseType: 1, 
  District_encoded: 1, Temperature: 37.5,
  Symptoms: 0, Platelet_Count: 150000, WBC_Count: 7500
};
fetch('http://localhost:5000/api/dengue/predict', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify(testData)
})
.then(r => r.json())
.then(d => console.log('Prediction:', d))
```

Expected output:
```json
{
  "prediction": 0 or 1,
  "probability": 0.2-0.9,
  "risk_level": "Low Risk" or "High Risk",
  "confidence": 0.2-0.9
}
```

---

## 🆘 Still Having Issues?

### Step-by-Step Recovery

1. **Clear Everything**:
   ```bash
   # Stop all processes (Ctrl+C)
   # Clear browser cache (Ctrl+Shift+Delete)
   # Restart backend: python main.py api
   # Restart frontend: npm start
   ```

2. **Retrain Models**:
   ```bash
   # If predictions are still failing
   python main.py train-all
   ```

3. **Check System**:
   ```bash
   # Verify Python version
   python --version  # Should be 3.8+
   
   # Verify Node version
   node --version    # Should be 14+
   
   # Check ports are free
   # 3000 for React
   # 5000 for Flask
   ```

4. **Nuclear Option**:
   ```bash
   # Delete all models and retrain
   rm -rf backend/models/*.h5
   python main.py train-all
   ```

---

**Remember**: Most issues are resolved by:
1. Restarting both backend and frontend
2. Clearing browser cache
3. Making sure all required fields are filled
4. Checking that values are numeric

Good luck! 🚀
