# DRF & Django Concepts - Complete Index

## 📚 Table of Contents

This index links to all concept documentation files, organized by topic.

---

## 🌐 Fundamentals

### [01-api-fundamentals.md](01-api-fundamentals.md)
**Topics Covered:**
- API & REST API Fundamentals
- Django Project Structure
- Django Settings for REST APIs
- Installed Apps & Middleware
- URL Routing Basics
- MVT vs MVC
- RESTful Naming Conventions
- Idempotent APIs
- Idempotency Keys
- Important SQL Queries

**When to read:** Start here! Understanding APIs, REST principles, and Django structure.

---

### [02-http-fundamentals.md](02-http-fundamentals.md)
**Topics Covered:**
- HTTP Request-Response Lifecycle
- HTTP Methods (GET, POST, PUT, PATCH, DELETE)
- HTTP Status Codes
- Request Object
- Response Object
- Content Negotiation
- Headers Handling
- Query Params vs Body Params

**When to read:** Understand how HTTP works and how requests/responses flow.

---

## 🎯 Views & Routing

### [03-views.md](03-views.md)
**Topics Covered:**
- Function Based Views (FBV)
- APIView
- Class Based Views (CBV)
- GenericAPIView
- Mixins
- ViewSets
- ModelViewSet
- Custom Actions (@action)
- Routers (Simple / Default)
- View Lifecycle (dispatch)
- Request Lifecycle in DRF

**When to read:** Learn how to create API endpoints and handle requests.

---

## 📝 Data Serialization

### [04-serializers.md](04-serializers.md)
**Topics Covered:**
- Serializer
- ModelSerializer
- Fields & Field Types
- read_only, write_only
- Validation (Field-level & Object-level)
- Custom Validators
- SerializerMethodField
- Dynamic Fields in Serializers
- Conditional Serialization
- Nested Serializers
- Writable Nested Serializers
- to_representation()
- create() & update() Overrides

**When to read:** Learn how to convert between Python objects and JSON.

---

## 🔐 Security & Access Control

### [05-authentication-authorization.md](05-authentication-authorization.md)
**Topics Covered:**
- Session Authentication
- Basic Authentication
- Token Authentication
- JWT Authentication
- OAuth2
- OpenID Connect (OIDC)
- Custom Authentication Classes
- Permission Classes
- Built-in Permissions
- Custom Permissions
- Object-level Permissions
- Role-Based Access Control (RBAC)
- Policy-Based Permissions

**When to read:** Understand how to secure your API and control access.

---

### [08-security.md](08-security.md)
**Topics Covered:**
- CSRF Protection
- CORS Configuration
- HTTPS Enforcement
- Sensitive Data Masking
- Encryption at Rest
- Encryption in Transit
- Prevent CWE-319 / CWE-352
- Input Sanitization
- Secure Headers

**When to read:** Learn security best practices for production APIs.

---

## 🔍 Data Management

### [06-filtering-pagination.md](06-filtering-pagination.md)
**Topics Covered:**
- DjangoFilterBackend
- SearchFilter
- OrderingFilter
- Custom Filters
- Dynamic Filtering
- PageNumberPagination
- LimitOffsetPagination
- CursorPagination
- Custom Pagination
- Custom Pagination Metadata

**When to read:** Learn how to filter, search, sort, and paginate API responses.

---

### [07-database-orm.md](07-database-orm.md)
**Topics Covered:**
- ORM Queries in APIs
- select_related()
- prefetch_related()
- N+1 Query Problems
- Query Optimization
- Atomic Transactions
- @transaction.atomic
- Multi-Database Support

**When to read:** Optimize database queries and handle transactions.

---

## 🚦 Performance & Limits

### [09-throttling-rate-limiting.md](09-throttling-rate-limiting.md)
**Topics Covered:**
- Anonymous Throttling
- User-based Throttling
- Scoped Throttling
- Custom Throttles
- Per-role/per-API Limits

**When to read:** Learn how to prevent API abuse and limit request rates.

---

## 📖 Learning Path

### For Beginners:
1. **Start Here:** [01-api-fundamentals.md](01-api-fundamentals.md)
2. **Then:** [02-http-fundamentals.md](02-http-fundamentals.md)
3. **Next:** [03-views.md](03-views.md)
4. **Then:** [04-serializers.md](04-serializers.md)
5. **Finally:** [05-authentication-authorization.md](05-authentication-authorization.md)

### For Intermediate:
1. [06-filtering-pagination.md](06-filtering-pagination.md)
2. [07-database-orm.md](07-database-orm.md)
3. [09-throttling-rate-limiting.md](09-throttling-rate-limiting.md)

### For Advanced:
1. [08-security.md](08-security.md)
2. Review all files for advanced patterns

---

## 🔍 Quick Reference

**Need to find a specific concept?**

- **API Basics** → [01-api-fundamentals.md](01-api-fundamentals.md)
- **HTTP** → [02-http-fundamentals.md](02-http-fundamentals.md)
- **Views** → [03-views.md](03-views.md)
- **Serializers** → [04-serializers.md](04-serializers.md)
- **Auth** → [05-authentication-authorization.md](05-authentication-authorization.md)
- **Filtering** → [06-filtering-pagination.md](06-filtering-pagination.md)
- **Database** → [07-database-orm.md](07-database-orm.md)
- **Security** → [08-security.md](08-security.md)
- **Rate Limiting** → [09-throttling-rate-limiting.md](09-throttling-rate-limiting.md)

---

## 📝 Notes

- All files follow the same format: **Definition** → **Real-life example** → **Code example**
- Each concept is explained in simple terms first
- Real project examples are provided where applicable
- Code examples are production-ready patterns

---

### [10-testing.md](10-testing.md)
**Topics Covered:**
- APITestCase
- APIClient
- Authentication testing
- Permission testing
- Serializer testing
- Mocking external APIs

**When to read:** Learn how to write comprehensive tests for your API.

---

### [11-caching.md](11-caching.md)
**Topics Covered:**
- Django caching
- API response caching
- Per-view caching
- Redis basics
- Cache invalidation strategies

**When to read:** Optimize API performance with caching.

---

### [12-file-uploads.md](12-file-uploads.md)
**Topics Covered:**
- File upload APIs
- Image handling
- File validation
- Streaming downloads
- Large file optimization

**When to read:** Learn how to handle file uploads efficiently.

---

### [13-bulk-operations.md](13-bulk-operations.md)
**Topics Covered:**
- Bulk create APIs
- Bulk update APIs
- Upsert APIs (Create or Update)
- Partial updates
- Soft delete
- Hard delete
- Restore APIs

**When to read:** Learn efficient ways to handle multiple objects.

---

### [14-versioning.md](14-versioning.md)
**Topics Covered:**
- URL versioning
- Header versioning
- Namespace versioning
- Versioned serializers & views
- Backward compatibility

**When to read:** Manage API evolution and multiple versions.

---

### [15-exception-handling.md](15-exception-handling.md)
**Topics Covered:**
- DRF default exceptions
- Custom exception classes
- Global exception handler
- Error format standardization

**When to read:** Handle errors consistently across your API.

---

### [16-parsers-renderers.md](16-parsers-renderers.md)
**Topics Covered:**
- JSONParser
- FormParser
- MultiPartParser
- Custom parser
- JSONRenderer
- BrowsableAPIRenderer
- Custom renderer
- Custom Response class

**When to read:** Understand how requests/responses are processed.

---

### [17-api-documentation.md](17-api-documentation.md)
**Topics Covered:**
- Browsable API
- OpenAPI schema
- Swagger integration
- drf-yasg
- drf-spectacular
- Versioned docs

**When to read:** Create comprehensive API documentation.

---

### [18-async-background-jobs.md](18-async-background-jobs.md)
**Topics Covered:**
- Async views
- Django async support
- Celery integration
- Background jobs
- Task retries & idempotency

**When to read:** Handle long-running tasks and async operations.

---

### [19-monitoring-logging.md](19-monitoring-logging.md)
**Topics Covered:**
- API logging
- Audit logs
- Error tracking
- Monitoring concepts
- Metrics exposure

**When to read:** Monitor and debug your API in production.

---

### [20-advanced-patterns.md](20-advanced-patterns.md)
**Topics Covered:**
- Multi-tenant APIs
- API Gateway concepts
- Webhooks
- Feature flags
- API deprecation strategy
- Backward compatibility strategy
- Error code standards
- Response consistency
- Large dataset streaming responses

**When to read:** Advanced patterns for production APIs.

---

**Last Updated:** All topic files created and documented
**Total Files:** 20 comprehensive topic files
**Format:** Each file is self-contained and can be read independently

