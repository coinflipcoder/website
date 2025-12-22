def on_starting(server):
  # This runs only once, not for every worker
  from database_handler import createTables
  createTables()

  import consts
  from datetime import datetime
  consts.DEPLOY_TIMESTAMP = datetime.now().strftime('%d.%m.%Y %H:%M:%S')