## Task:

### Implement an API endpoint for the scenario below:

- Imagine that a frontend design has been drafted to present data that we already have in our DB: `Posts` and `Comments`.

  - The design is an infinite scrolling list of `Posts`.

- The list of `Posts` should be ordered by timestamp, latest first.

- Some `Posts` will have `Comments`.

- For each `Post` in this list, we want to show up to 3 `Comments` for that `Post` (`Comments` also sorted latest first).

  - For each `Post`: we will need to display a `Post`'s text, timestamp, `Comment` count, and author's username.

  - For `Comments`: we will need to display a `Comment`'s text, timestamp, and author's username.

- Include basic documentation on how to use your new endpoint.

### Follow-up Q:

- Instead of sorting comments by timestamp, how would you fetch 3 random comments associated to a given post?
  - You can leave your answer anywhere in the project codebase that you deem appropriate.

---

## To get started:

1. Set up a virtualenv for this project (The author used Python 3.10.14)

- Example: `pyenv local myvirtualenv` (or however you set up Python virtualenvs)

2. Install dependencies: `pip install -r requirements.txt`

3. Migrate database `python manage.py migrate`

4. Now head to apps/demo/views.py and complete the assignment!

- Run tests via `python manage.py test apps` or
- check server after running via `python manage.py runserver`

Here is a basic markdown document explaining how to use the new `Post List API` endpoint, including details about the request and response format, as well as pagination and the comment count feature.

---

## Basic Documentation Post List API

### Endpoint

```
GET /posts/
```

### Description

This endpoint retrieves a paginated list of posts along with their associated comments. Each post includes metadata like the total number of comments (`comment_count`) and the latest 3 comments ordered by timestamp.

### Query Parameters

- **page**: The page number to fetch. (Default is `1`).
- **page_size**: The number of posts per page. (Default is `10`, maximum is `100`).

### Example Request

```
GET /posts/?page=1&page_size=5
```

### Response Format

The response will return a paginated list of posts, each with the following fields:

- **id**: UUID of the post.
- **text**: The text content of the post.
- **timestamp**: The timestamp when the post was created.
- **user**: The username of the user who created the post.
- **comment_count**: The total number of comments associated with the post.
- **comments**: A list of up to 3 comments for the post, ordered by the most recent first. Each comment includes:
  - **id**: UUID of the comment.
  - **text**: The text content of the comment.
  - **timestamp**: The timestamp when the comment was created.
  - **user**: The username of the comment's author.

### Example Response

```json
{
  "count": 2,
  "next": "http://example.com/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": "5a4f03f0-7b92-4f79-987a-635276c28e16",
      "text": "Post 1 text",
      "timestamp": "2024-12-28T13:58:25.643312Z",
      "user": "user1",
      "comment_count": 3,
      "comments": [
        {
          "id": "e4ad9688-38fc-4625-b94f-d7ea7e63360c",
          "text": "Comment 3 for Post 1",
          "timestamp": "2024-12-28T13:57:20.454443Z",
          "user": "user2"
        },
        {
          "id": "a8be2380-3983-44d4-9d84-84b9d4f31e90",
          "text": "Comment 2 for Post 1",
          "timestamp": "2024-12-28T13:56:20.454723Z",
          "user": "user1"
        },
        {
          "id": "8a531e0d-49bc-4f64-b2b1-322e4ed42ad7",
          "text": "Comment 1 for Post 1",
          "timestamp": "2024-12-28T13:55:20.454723Z",
          "user": "user2"
        }
      ]
    },
    {
      "id": "9e8d5e0f-2440-47ab-b8fc-776b8182b213",
      "text": "Post 2 text",
      "timestamp": "2024-12-28T13:58:25.643312Z",
      "user": "user2",
      "comment_count": 1,
      "comments": [
        {
          "id": "5a244a27-90f1-4513-b3bb-835ee0a10cc7",
          "text": "Comment 1 for Post 2",
          "timestamp": "2024-12-28T13:54:20.454723Z",
          "user": "user1"
        }
      ]
    }
  ]
}
```

### Notes

- **Pagination**: The response is paginated, and you can navigate through the pages using the `next` and `previous` links provided in the response.
- **Comments**: By default, each post will return up to 3 comments, sorted by timestamp in descending order (latest first).
- **Comment Count**: The `comment_count` field provides the total number of comments associated with a post.

### Example of Handling Pagination

For pagination, if you request `/posts/?page=1&page_size=5` and there are more than 5 posts, you will receive a `next` URL in the response to access the next page of posts:

```json
{
  "count": 15,
  "next": "http://example.com/posts/?page=2&page_size=5",
  "previous": null,
  "results": [
    // First 5 posts
  ]
}
```

To retrieve the next set of posts, you can make a request to the URL in the `next` field.

---

### Running Tests

To run the tests for this API endpoint and verify the functionality, you can run the following command:

```bash
python manage.py test apps.demo.tests
```

This will run the full test suite, including tests for:

- Pagination of posts.
- Comment count correctness.
- Sorting of posts by timestamp.
- Comment ordering (latest first).
