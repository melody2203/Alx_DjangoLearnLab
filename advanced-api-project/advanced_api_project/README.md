# Advanced API Project - Custom Views Documentation

## View Configurations

### Book Views

1. **BookListView** (`/api/books/`)
   - **Purpose**: Retrieve all books
   - **Methods**: GET
   - **Permissions**: Read-only access for all users
   - **Features**: 
     - Filtering by `publication_year` and `author`
     - Search by `title` and `author__name`
     - Ordering by `title` and `publication_year`

2. **BookDetailView** (`/api/books/<int:pk>/`)
   - **Purpose**: Retrieve single book by ID
   - **Methods**: GET
   - **Permissions**: Read-only access for all users

3. **BookCreateView** (`/api/books/create/`)
   - **Purpose**: Create new book
   - **Methods**: POST
   - **Permissions**: Authenticated users only
   - **Custom Behavior**: Enhanced response with success message

4. **BookUpdateView** (`/api/books/<int:pk>/update/`)
   - **Purpose**: Update existing book
   - **Methods**: PUT, PATCH
   - **Permissions**: Authenticated users only
   - **Custom Behavior**: Enhanced response with success message

5. **BookDeleteView** (`/api/books/<int:pk>/delete/`)
   - **Purpose**: Delete book
   - **Methods**: DELETE
   - **Permissions**: Authenticated users only

### Custom Settings and Hooks

- **Filtering**: Integrated Django Filter for field-based filtering
- **Search**: Full-text search on book titles and author names
- **Ordering**: Multiple field ordering with default by title
- **Permissions**: Custom permission classes for granular access control
- **Response Format**: Custom response format with messages and data

## Testing Guidelines

Use the following endpoints for testing:

```bash
# List all books (public access)
GET /api/books/

# Get specific book (public access)
GET /api/books/1/

# Create book (authenticated only)
POST /api/books/create/

# Update book (authenticated only)
PUT /api/books/1/update/

# Delete book (authenticated only)
DELETE /api/books/1/delete/