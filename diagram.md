# Діаграма сутність-зв'язок (ER Diagram)

Діаграма відображає структуру бази даних бібліотеки з двома сутностями:
**Author** (автор) та **Book** (книга), пов'язаними відношенням «один до багатьох».

```mermaid
erDiagram
    AUTHORS ||--o{ BOOKS : "has many"

    AUTHORS {
        INTEGER id PK "Primary Key, Autoincrement"
        TEXT full_name "NOT NULL — Повне ім'я автора"
        TEXT bio "NOT NULL DEFAULT '' — Біографія"
    }

    BOOKS {
        INTEGER id PK "Primary Key, Autoincrement"
        TEXT title "NOT NULL — Назва книги"
        INTEGER published_year "NOT NULL — Рік публікації"
        INTEGER author_id FK "NOT NULL — Foreign Key -> AUTHORS(id)"
    }
```

## Опис зв'язків

| Зв'язок | Тип | Опис |
|---------|-----|------|
| `AUTHORS` → `BOOKS` | One-to-Many | Один автор може мати багато книг |
| `BOOKS.author_id` → `AUTHORS.id` | Foreign Key | Зовнішній ключ з каскадним оновленням та видаленням |
