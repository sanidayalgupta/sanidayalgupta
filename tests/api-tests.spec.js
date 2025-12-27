/**
 * Playwright Tests for DRF Tutorial API
 * 
 * These tests automatically check if the API is working correctly.
 * Like a robot that visits your website and clicks buttons to make sure everything works.
 * 
 * To run: npx playwright test
 */

const { test, expect } = require('@playwright/test');

// Test the basics API endpoints
test.describe('Basics API Tests', () => {
  test('should list students', async ({ request }) => {
    // Make a GET request to list students
    // Like visiting a webpage to see a list
    const response = await request.get('/api/basics/students-fbv/');
    
    // Check if the response is successful (status 200 = OK)
    expect(response.ok()).toBeTruthy();
    
    // Check if we got JSON data back
    const data = await response.json();
    expect(Array.isArray(data)).toBeTruthy();
  });

  test('should create a student', async ({ request }) => {
    // Create a new student
    // Like filling out a form and submitting it
    const response = await request.post('/api/basics/students-fbv/', {
      data: {
        name: 'Test Student',
        email: 'test@example.com',
        age: 20,
        grade: 'A'
      }
    });
    
    // Check if creation was successful (status 201 = Created)
    expect(response.status()).toBe(201);
    
    // Check if we got the student data back
    const data = await response.json();
    expect(data.name).toBe('Test Student');
    expect(data.email).toBe('test@example.com');
  });

  test('should get student detail', async ({ request }) => {
    // First create a student
    const createResponse = await request.post('/api/basics/students-fbv/', {
      data: {
        name: 'Detail Test',
        email: 'detail@example.com',
        age: 21,
        grade: 'B'
      }
    });
    
    const student = await createResponse.json();
    const studentId = student.id;
    
    // Then get the student details
    const getResponse = await request.get(`/api/basics/students-fbv/${studentId}/`);
    
    // Check if we got the student
    expect(getResponse.ok()).toBeTruthy();
    const data = await getResponse.json();
    expect(data.id).toBe(studentId);
    expect(data.name).toBe('Detail Test');
  });
});

// Test intermediate API endpoints
test.describe('Intermediate API Tests', () => {
  test('should list books', async ({ request }) => {
    const response = await request.get('/api/intermediate/books/');
    expect(response.ok()).toBeTruthy();
    
    const data = await response.json();
    // ViewSets return paginated results
    expect(data).toHaveProperty('results');
  });
});

// Test that the API is accessible
test.describe('API Accessibility', () => {
  test('basics API should be accessible', async ({ request }) => {
    const response = await request.get('/api/basics/students-fbv/');
    expect(response.status()).toBe(200);
  });

  test('intermediate API should be accessible', async ({ request }) => {
    const response = await request.get('/api/intermediate/books/');
    expect(response.status()).toBe(200);
  });
});

