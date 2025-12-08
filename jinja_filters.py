def create_filters(app):
  app.jinja_env.filters['langicon'] = map_language_to_icon

LANGUAGE_MAPPING = {
  "python": "\ue73c",
  "html": "\ue736",
  "css": "\ue749",
  "java": "\ue738",
  "nextjs": "\ue83e"
}

#
# Custom Jinja filters
#
def map_language_to_icon(lang):
  return LANGUAGE_MAPPING.get(lang, "?")