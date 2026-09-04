# Git conventions
- Message format: `"[<app_or_label>] feat/fix: <message>"`
  Examples:
    * If commits contain general changes: `"[general] feat/fix: <message>"`
    * If commits contain changes related only to one app: `"[<app>] feat/fix: <message>"`
- Branch naming: branch has the name related to the feature/fix it does with ordering.
  Examples:
    * `fix/<order>/<some_functionality>`, e.g. `fix/1/order-processing`, `fix/2/migrate-to-new-django-version`
    * `feat/<order>/<some_functionality>`, e.g. `feat/1/authentication`, `feat/2/user-profiles`