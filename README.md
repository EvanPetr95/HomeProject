# Home Project

## Getting Started
The Service Consists of several components:
- Flask Web Application – Serves as the main API layer, handling HTTP requests and routing.
- GraphQL API – Provides a flexible query interface on top of the data layer, allowing clients to request exactly the data they need. Implemented using Strawberry GraphQL integrated with Flask.
- PostgresSQL Database – Manages data persistence, supporting relational data models and ensuring consistency across the service.

### Run App
```
$ make run
```

### Seed DB with data
```
$ make db.seed
```

### Clear DB from data
```
$ make db.clear
```

### Connect to database
Creds:
- user: postgres
- password: pass
- db: vee

```
$ make db.shell
```

### Stop App
```
$ make stop
```

### Run linter
```
$ make lint
```

### Run tests
```
$ make test
```

### Run tests coverage
```
$ make test.coverage
```