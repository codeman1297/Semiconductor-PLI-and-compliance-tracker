# Data model

`companies` and `locations` normalize project ownership and geography. `projects` stores the current reviewed view and publication state. `sources` attach evidence to a project. `milestones` preserve independent lifecycle stages, while `project_history` stores material field changes. `raw_sources` holds untrusted intake for future processing. A project can only be created through the API with at least one source; publication is a separate administrative decision.
