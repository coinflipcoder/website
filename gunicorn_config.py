def on_starting(server):
  # This runs only once, not for every worker
  from database_handler import createTables
  createTables()
