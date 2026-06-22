# DVD

## Columns

| Name | Type | Null | Key | Default | Extra |
|------|------|------|-----|---------|-------|
| id | int | NO | PRI | None | auto_increment |
| nome | varchar(150) | NO | / | None | / |
| durata | int | NO | / | None | / |
| regista | varchar(100) | NO | / | None | / |
| prezzo | decimal(10,2) | YES | / | None | / |
| inCatalogo | tinyint(1) | YES | / | 1 | / |

### Constraints

| Name | Type |
|------|------|
| PRIMARY | PRIMARY KEY |

### Indexes

| Name | Column | Unique |
|------|--------|--------|
| PRIMARY | id | Yes |


---
# INDIRIZZO

## Columns

| Name | Type | Null | Key | Default | Extra |
|------|------|------|-----|---------|-------|
| id | int unsigned | NO | PRI | None | auto_increment |
| seqId | varchar(36) | NO | / | None | / |
| userID | int | NO | MUL | None | / |
| nome | varchar(100) | NO | / | None | / |
| cognome | varchar(100) | NO | / | None | / |
| indirizzo | varchar(255) | NO | / | None | / |
| citta | varchar(100) | NO | / | None | / |
| cap | varchar(10) | NO | / | None | / |
| paese | char(2) | NO | / | IT | / |

### Foreign Keys

- **userID** → UTENTE(id)

### Constraints

| Name | Type |
|------|------|
| PRIMARY | PRIMARY KEY |
| INDIRIZZO_ibfk_1 | FOREIGN KEY |

### Indexes

| Name | Column | Unique |
|------|--------|--------|
| PRIMARY | id | Yes |
| userID | userID | No |


---
# ORDINE

## Columns

| Name | Type | Null | Key | Default | Extra |
|------|------|------|-----|---------|-------|
| id | int | NO | PRI | None | auto_increment |
| utente_id | int | NO | MUL | None | / |
| seqId | varchar(36) | NO | UNI | None | / |
| data_ordine | timestamp | YES | / | CURRENT_TIMESTAMP | DEFAULT_GENERATED |

### Foreign Keys

- **utente_id** → UTENTE(id)

### Constraints

| Name | Type |
|------|------|
| PRIMARY | PRIMARY KEY |
| uq_seqId | UNIQUE |
| ORDINE_ibfk_1 | FOREIGN KEY |

### Indexes

| Name | Column | Unique |
|------|--------|--------|
| PRIMARY | id | Yes |
| uq_seqId | seqId | Yes |
| utente_id | utente_id | No |


---
# ORDINE_DVD

## Columns

| Name | Type | Null | Key | Default | Extra |
|------|------|------|-----|---------|-------|
| ordine_id | int | NO | PRI | None | / |
| dvd_id | int | NO | PRI | None | / |
| quantita | int | NO | / | 1 | / |
| prezzo_unitario | decimal(10,2) | NO | / | None | / |

### Foreign Keys

- **ordine_id** → ORDINE(id)
- **dvd_id** → DVD(id)

### Constraints

| Name | Type |
|------|------|
| PRIMARY | PRIMARY KEY |
| ORDINE_DVD_ibfk_1 | FOREIGN KEY |
| ORDINE_DVD_ibfk_2 | FOREIGN KEY |

### Indexes

| Name | Column | Unique |
|------|--------|--------|
| dvd_id | dvd_id | No |
| PRIMARY | ordine_id | Yes |
| PRIMARY | dvd_id | Yes |


---
# UTENTE

## Columns

| Name | Type | Null | Key | Default | Extra |
|------|------|------|-----|---------|-------|
| id | int | NO | PRI | None | auto_increment |
| email | varchar(100) | NO | UNI | None | / |
| username | varchar(50) | NO | UNI | None | / |
| password | varchar(255) | NO | / | None | / |
| admin | tinyint(1) | YES | / | 0 | / |

### Constraints

| Name | Type |
|------|------|
| PRIMARY | PRIMARY KEY |
| uq_email | UNIQUE |
| uq_username | UNIQUE |

### Indexes

| Name | Column | Unique |
|------|--------|--------|
| PRIMARY | id | Yes |
| uq_email | email | Yes |
| uq_username | username | Yes |


---
