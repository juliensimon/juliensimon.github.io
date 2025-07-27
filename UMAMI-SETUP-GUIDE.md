# Umami Analytics Setup Guide
## Julien Simon's Website - www.julien.org

**Last Updated:** January 18, 2025  
**Website ID:** `27550dad-d418-4f5d-ad1b-dab573da1020`

---

## 🔧 **Issues Fixed**

### 1. **Inconsistent Website IDs**
- **Problem:** Different pages were using different website IDs
- **Solution:** Standardized all pages to use `27550dad-d418-4f5d-ad1b-dab573da1020`

### 2. **Missing Analytics on Key Pages**
- **Problem:** `aws-medium-posts.html`, `medium-blog-posts.html`, `huggingface-blog-posts.html` had no Umami script
- **Solution:** Added consistent Umami script to all pages

### 3. **Performance Issues**
- **Problem:** Main page loaded Umami after page load (missed early pageviews)
- **Solution:** Changed to immediate loading with `defer` attribute

### 4. **Inconsistent Loading Methods**
- **Problem:** Some pages used `async defer`, others used dynamic injection
- **Solution:** Standardized to `defer` attribute across all pages

---

## 📊 **Current Setup**

### **Standard Implementation (All Pages)**
```html
<!-- Umami Analytics -->
<script defer src="https://cloud.umami.is/script.js" data-website-id="27550dad-d418-4f5d-ad1b-dab573da1020"></script>
```

### **Content Security Policy**
```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://cloud.umami.is https://maps.googleapis.com https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com; font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com; img-src 'self' data: https: blob:; connect-src 'self' https://cloud.umami.is https://maps.googleapis.com; frame-src https://www.youtube.com; object-src 'none'; base-uri 'self'; form-action 'self'; upgrade-insecure-requests;">
```

### **DNS Prefetch**
```html
<link rel="dns-prefetch" href="//cloud.umami.is">
<link rel="preconnect" href="https://cloud.umami.is">
```

---

## 🧪 **Testing & Verification**

### **1. Browser Console Test**
Open browser console and look for:
```
🔍 Testing Umami Analytics...
✅ Umami script found: https://cloud.umami.is/script.js
✅ Umami object available
✅ Umami tracking test successful
```

### **2. Network Tab Verification**
1. Open Developer Tools → Network tab
2. Refresh page
3. Look for requests to `cloud.umami.is`
4. Should see successful 200 responses

### **3. Umami Dashboard Check**
1. Login to your Umami dashboard
2. Check for real-time visitors
3. Verify pageviews are being recorded
4. Check for any error messages

---

## 📈 **Expected Analytics Data**

### **Page Views**
- Homepage visits
- Individual page visits (experience, speaking, publications, etc.)
- Blog post visits
- Speaking engagement page visits

### **Custom Events**
- Web Vitals tracking (LCP, FID, CLS, INP)
- Performance metrics
- Error tracking
- User interactions

### **Traffic Sources**
- Direct traffic
- Search engine referrals
- Social media referrals
- External link referrals

---

## 🔍 **Troubleshooting**

### **No Data in Dashboard**
1. **Check Website ID:** Verify `27550dad-d418-4f5d-ad1b-dab573da1020` is correct
2. **Check CSP:** Ensure `https://cloud.umami.is` is allowed in script-src and connect-src
3. **Check Script Loading:** Verify script loads without errors in console
4. **Check Network:** Ensure no network errors in Developer Tools

### **Partial Data**
1. **Check Individual Pages:** Some pages might have different implementations
2. **Check Ad Blockers:** Users with ad blockers might not send data
3. **Check Privacy Settings:** Some browsers block analytics by default

### **Performance Issues**
1. **Use `defer` attribute:** Prevents blocking page rendering
2. **DNS prefetch:** Speeds up connection to Umami servers
3. **Preconnect:** Establishes connection early

---

## 📱 **Mobile & Privacy Considerations**

### **Mobile Performance**
- Script loads asynchronously with `defer`
- Minimal impact on page load time
- DNS prefetch reduces connection time

### **Privacy Compliance**
- Umami is GDPR compliant
- No cookies used by default
- Respects Do Not Track headers
- Can be configured for privacy-first analytics

### **Ad Blocker Resistance**
- Umami is less likely to be blocked than Google Analytics
- Self-hosted option available if needed
- Privacy-focused approach reduces blocking

---

## 🚀 **Optimization Recommendations**

### **1. Enhanced Tracking**
```javascript
// Track custom events
umami.track('button_click', { button: 'github_link' });
umami.track('form_submit', { form: 'contact' });
umami.track('video_play', { video: 'youtube_intro' });
```

### **2. Performance Monitoring**
```javascript
// Track Core Web Vitals
umami.track('web_vital', {
  metric: 'LCP',
  value: 1200,
  page: window.location.pathname
});
```

### **3. Error Tracking**
```javascript
// Track JavaScript errors
window.addEventListener('error', (event) => {
  umami.track('error', {
    message: event.message,
    filename: event.filename,
    lineno: event.lineno
  });
});
```

---

## 📞 **Support & Maintenance**

### **Regular Checks**
- Weekly: Check dashboard for data consistency
- Monthly: Review traffic patterns and sources
- Quarterly: Update tracking implementation if needed

### **Contact Information**
- **Umami Support:** https://umami.is/docs
- **Website Owner:** julien@julien.org
- **Technical Issues:** Check browser console and network tab

---

## 📋 **Implementation Checklist**

- [x] Standardized website ID across all pages
- [x] Added Umami script to all HTML pages
- [x] Configured Content Security Policy
- [x] Added DNS prefetch and preconnect
- [x] Implemented performance monitoring
- [x] Added error tracking
- [x] Created test script for verification
- [x] Documented setup and troubleshooting

---

**Note:** This setup should now provide comprehensive analytics coverage across your entire website. Monitor the dashboard for the next 24-48 hours to confirm data is being collected properly. 