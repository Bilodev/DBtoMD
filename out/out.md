# DVD
##### id:
- **type**: int
- **null**: NO
- **key**: PRI
- **default**: None
- **extra**: auto_increment
##### nome:
- **type**: varchar(150)
- **null**: NO
- **key**: /
- **default**: None
- **extra**: /
##### durata:
- **type**: int
- **null**: NO
- **key**: /
- **default**: None
- **extra**: /
##### regista:
- **type**: varchar(100)
- **null**: NO
- **key**: /
- **default**: None
- **extra**: /
##### inCatalogo:
- **type**: tinyint(1)
- **null**: YES
- **key**: /
- **default**: 1
- **extra**: /
##### prezzo:
- **type**: decimal(10,0)
- **null**: YES
- **key**: /
- **default**: None
- **extra**: /
# ORDINE
##### id:
- **type**: int
- **null**: NO
- **key**: PRI
- **default**: None
- **extra**: auto_increment
##### utente_id:
- **type**: int
- **null**: NO
- **key**: MUL
- **default**: None
- **extra**: /
##### dvd_id:
- **type**: int
- **null**: NO
- **key**: MUL
- **default**: None
- **extra**: /
##### prezzo:
- **type**: decimal(10,2)
- **null**: NO
- **key**: /
- **default**: None
- **extra**: /
##### data_ordine:
- **type**: timestamp
- **null**: YES
- **key**: /
- **default**: CURRENT_TIMESTAMP
- **extra**: DEFAULT_GENERATED
##### quantita:
- **type**: int
- **null**: YES
- **key**: /
- **default**: 1
- **extra**: /
# UTENTE
##### id:
- **type**: int
- **null**: NO
- **key**: PRI
- **default**: None
- **extra**: auto_increment
##### email:
- **type**: varchar(100)
- **null**: NO
- **key**: UNI
- **default**: None
- **extra**: /
##### username:
- **type**: varchar(50)
- **null**: NO
- **key**: UNI
- **default**: None
- **extra**: /
##### password:
- **type**: varchar(255)
- **null**: NO
- **key**: /
- **default**: None
- **extra**: /
##### admin:
- **type**: tinyint(1)
- **null**: YES
- **key**: /
- **default**: 0
- **extra**: /
