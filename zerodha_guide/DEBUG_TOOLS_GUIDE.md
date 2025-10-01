# ZERODHA API DEBUG TOOLS GUIDE

## 🔧 Overview

This guide explains the debug tools included with the Zerodha API implementation. These tools help you troubleshoot issues, understand API responses, and develop applications more effectively.

## 📁 Debug Tools Available

### 1. `debug_api.py` - Comprehensive API Diagnostic Tool

**Purpose:** Complete API debugging and diagnostics

**Features:**
- ✅ Environment variable validation
- ✅ API credential verification  
- ✅ Network connectivity testing
- ✅ Response structure analysis
- ✅ Detailed error reporting
- ✅ Authentication troubleshooting

**Usage:**
```bash
python debug_api.py
```

**When to Use:**
- First time API setup
- Authentication errors
- Network connectivity issues
- API response errors
- Environment configuration problems

---

### 2. `debug_responses.py` - Response Structure Analyzer

**Purpose:** Analyze and understand API response structures

**Features:**
- ✅ Response type analysis
- ✅ Content structure inspection
- ✅ Data format understanding
- ✅ Response validation
- ✅ Data parsing assistance

**Usage:**
```bash
python debug_responses.py
```

**When to Use:**
- Understanding API response formats
- Debugging data parsing issues
- Development and testing
- Response structure analysis
- Building data processing logic

---

## 🚀 Quick Start Guide

### Step 1: Initial Setup Check
```bash
# Check if everything is configured correctly
python debug_api.py
```

**Expected Output:**
```
🔍 DEBUGGING ZERODHA API SETUP
1️⃣ Environment Variables:
ZERODHA_API_KEY: ✅ Set
ZERODHA_ACCESS_TOKEN: ✅ Set

2️⃣ .env File Check:
✅ .env file exists
✅ ZERODHA_API_KEY found in .env

3️⃣ API Response Debug:
✅ Profile API call successful
```

### Step 2: Understand Response Format
```bash
# Analyze API response structures
python debug_responses.py
```

**Expected Output:**
```
🔍 DEBUGGING ZERODHA API RESPONSE STRUCTURES
1️⃣ QUOTES API RESPONSE:
Type: <class 'dict'>
Content: {'status': 'success', 'data': {'NSE:RELIANCE': {...}}}

2️⃣ PORTFOLIO API RESPONSE:
Type: <class 'dict'>
Content: {'status': 'success', 'data': [...]}
```

### Step 3: Test with Examples
```bash
# Run practical examples
python example_usage.py
```

---

## 🔍 Detailed Tool Descriptions

### `debug_api.py` - Complete Analysis

#### Environment Validation
- Checks for `ZERODHA_API_KEY` environment variable
- Checks for `ZERODHA_ACCESS_TOKEN` environment variable
- Validates `.env` file existence and content
- Shows partial credentials for verification

#### Network Connectivity Testing
- Tests basic connectivity to Zerodha API servers
- Validates API key authentication
- Checks for network timeouts and connection issues
- Provides HTTP status code analysis

#### API Response Analysis
- Tests profile API call
- Shows complete response structure
- Identifies response format issues
- Provides detailed error information

#### Error Diagnosis
- Detailed error reporting with error types
- HTTP status code analysis
- Network connectivity troubleshooting
- Authentication issue identification

### `debug_responses.py` - Response Analysis

#### Response Type Analysis
- Shows exact data types returned by API
- Identifies unexpected response formats
- Helps understand data structure

#### Content Structure Inspection
- Displays full response content
- Shows nested data structures
- Identifies key-value relationships

#### Data Format Understanding
- Helps understand how to parse responses
- Shows data access patterns
- Identifies required vs optional fields

---

## 🛠️ Common Issues & Solutions

### Issue 1: Authentication Errors

**Symptoms:**
```
❌ ZERODHA_API_KEY: Not Set
❌ ZERODHA_ACCESS_TOKEN: Not Set
❌ .env file not found
```

**Solution:**
1. Create `.env` file in your project root
2. Add your credentials:
   ```
   ZERODHA_API_KEY=your_api_key_here
   ZERODHA_ACCESS_TOKEN=your_access_token_here
   ```
3. Verify credentials are correct
4. Run `python debug_api.py` again

### Issue 2: Response Parsing Errors

**Symptoms:**
```
❌ 'user_name' not found in response
❌ Unexpected response type: <class 'str'>
❌ API returned unexpected format
```

**Solution:**
1. Run `python debug_responses.py` to understand structure
2. Access data using `response['data']` instead of `response` directly
3. Check for `status` field before processing data
4. Handle empty data arrays gracefully

### Issue 3: Network Connectivity Issues

**Symptoms:**
```
❌ Network test failed: Connection timeout
❌ API request failed: Connection error
❌ Basic connectivity: HTTP 500
```

**Solution:**
1. Check internet connection
2. Verify Zerodha server status
3. Check firewall settings
4. Try again during market hours
5. Contact Zerodha support if persistent

### Issue 4: API Response Format Issues

**Symptoms:**
```
❌ Quotes API returned unexpected format
❌ Portfolio API returned unexpected format
❌ Orders API returned unexpected format
```

**Solution:**
1. Run `python debug_responses.py` to see actual structure
2. Update your code to handle `{'status': 'success', 'data': [...]}` format
3. Check for `status` field before accessing `data`
4. Handle empty data arrays

---

## 📊 Debug Tool Comparison

| Feature | debug_api.py | debug_responses.py |
|---------|--------------|-------------------|
| **Environment Check** | ✅ | ❌ |
| **Network Testing** | ✅ | ❌ |
| **Response Analysis** | ✅ | ✅ |
| **Error Diagnosis** | ✅ | ❌ |
| **Data Structure** | ❌ | ✅ |
| **Format Understanding** | ❌ | ✅ |
| **Authentication** | ✅ | ❌ |
| **Content Inspection** | ✅ | ✅ |

---

## 🎯 Best Practices

### Development Workflow
1. **Always run debug tools first** when setting up API
2. **Use debug_responses.py** to understand data structures
3. **Check debug_api.py output** for authentication issues
4. **Run examples** to test your implementation
5. **Handle errors gracefully** in production code

### Debugging Process
1. **Start with `debug_api.py`** for initial setup
2. **Use `debug_responses.py`** for data structure issues
3. **Test with `example_usage.py`** for functionality
4. **Implement error handling** based on debug output

### Production Considerations
- Remove debug tools from production code
- Implement proper error handling
- Use debug output to understand error patterns
- Monitor API responses for changes

---

## 🔧 Advanced Usage

### Custom Debug Scripts
You can create custom debug scripts based on the provided tools:

```python
from zerodha_api_complete import ZerodhaAPI

def custom_debug():
    api = ZerodhaAPI()
    
    # Test specific endpoints
    try:
        profile = api.get_profile()
        print(f"Profile: {profile}")
    except Exception as e:
        print(f"Profile error: {e}")
    
    # Test market data
    try:
        quotes = api.get_quotes(["NSE:RELIANCE"])
        print(f"Quotes: {quotes}")
    except Exception as e:
        print(f"Quotes error: {e}")

if __name__ == "__main__":
    custom_debug()
```

### Integration with CI/CD
```bash
# Add to your build process
python debug_api.py > debug_output.txt
python debug_responses.py >> debug_output.txt
```

---

## 📞 Support

### Debug Tool Issues
- Check the debug output carefully
- Look for specific error messages
- Verify environment setup
- Test network connectivity

### API Issues
- Contact Zerodha support: connect@zerodha.com
- Check Zerodha status page
- Verify API documentation

### Development Issues
- Review debug tool output
- Check response structures
- Test with examples
- Implement proper error handling

---

**Last Updated:** January 2025  
**Version:** 1.0  
**Author:** AI Assistant
