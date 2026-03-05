// Umami Analytics Test Script
(function() {
  'use strict';
  
  // Test if Umami is loaded
  function testUmami() {
    console.log('🔍 Testing Umami Analytics...');
    
    // Check if Umami script is present
    const umamiScript = document.querySelector('script[src*="cloud.umami.is"]');
    if (umamiScript) {
      console.log('✅ Umami script found:', umamiScript.src);
    } else {
      console.error('❌ Umami script not found');
      return false;
    }
    
    // Check if Umami object exists
    if (typeof umami !== 'undefined') {
      console.log('✅ Umami object available');
      
      // Test tracking
      try {
        umami.track('test_event', {
          test: true,
          timestamp: Date.now(),
          page: window.location.pathname
        });
        console.log('✅ Umami tracking test successful');
        return true;
      } catch (error) {
        console.error('❌ Umami tracking failed:', error);
        return false;
      }
    } else {
      console.log('⏳ Umami not loaded yet, waiting...');
      
      // Wait for Umami to load
      setTimeout(() => {
        if (typeof umami !== 'undefined') {
          console.log('✅ Umami loaded after delay');
          testUmami();
        } else {
          console.error('❌ Umami failed to load after delay');
        }
      }, 2000);
      
      return false;
    }
  }
  
  // Run test when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', testUmami);
  } else {
    testUmami();
  }
  
  // Also test after page load
  window.addEventListener('load', () => {
    setTimeout(testUmami, 1000);
  });
  
})(); 