def create_filters(app):
  app.jinja_env.filters['langicon'] = map_language_to_icon



#
# Custom Jinja filters
#
def map_language_to_icon(lang):
  mapping = {
    "python": "\ue73c",
    "html": "\ue736",
    "css": "\ue749",
    "java": "\ue738",
    "nextjs": "\ue83e"
  }
  return mapping.get(lang, "?")