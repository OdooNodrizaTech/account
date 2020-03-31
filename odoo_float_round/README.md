El módulo realizar los siguientes updates directamente con el objetivo de evitar campos con +2 decimales que crean "confusión" a la hora de filtrar en las vistas de Odoo,

```
UPDATE account_move SET amount = ROUND(amount::numeric,3);
UPDATE account_move_line SET debit = ROUND(debit::numeric,3);
UPDATE account_move_line SET credit = ROUND(credit::numeric,3);
UPDATE account_move_line SET balance = ROUND(balance::numeric,3);
```

El módulo contiene el siguiente cron: Fix Odoo Floar Round  que ejecuta los updates.
