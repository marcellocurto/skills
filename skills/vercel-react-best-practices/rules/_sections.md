# Sections

This file defines all sections, their ordering, impact levels, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

Impact levels prioritize investigation when a mechanism applies; they are not measured application results or automatic review severity.

---

## 1. Eliminating Waterfalls (async)

**Impact:** CRITICAL  
**Description:** Remove sequential waits on the critical path when the operations are genuinely independent. The benefit depends on their durations and required ordering.

## 2. Bundle Size Optimization (bundle)

**Impact:** CRITICAL  
**Description:** Reducing initial bundle size improves Time to Interactive and Largest Contentful Paint.

## 3. Server-Side Performance (server)

**Impact:** HIGH  
**Description:** Optimizing server-side rendering and data fetching eliminates server-side waterfalls and reduces response times.

## 4. Client-Side Data Fetching (client)

**Impact:** MEDIUM-HIGH  
**Description:** Automatic deduplication and efficient data fetching patterns reduce redundant network requests.

## 5. Re-render Optimization (rerender)

**Impact:** MEDIUM  
**Description:** Reducing unnecessary re-renders minimizes wasted computation and improves UI responsiveness.

## 6. Rendering Performance (rendering)

**Impact:** MEDIUM  
**Description:** Optimizing the rendering process reduces the work the browser needs to do.

## 7. JavaScript Performance (js)

**Impact:** LOW-MEDIUM  
**Description:** Investigate repeated work on demonstrated hot paths; keep direct code when runtime savings do not justify additional machinery.

## 8. Advanced Patterns (advanced)

**Impact:** LOW  
**Description:** Advanced patterns for specific cases that require careful implementation.
