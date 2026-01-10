def on_starting(server):
  # This runs only once, not for every worker
  from scripts.database_handler import createTables
  createTables()

  import scripts.consts as consts
  from datetime import datetime
  consts.DEPLOY_TIMESTAMP = datetime.now().strftime('%d.%m.%Y %H:%M:%S')