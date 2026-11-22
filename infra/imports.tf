# The resources were created by hand in the bunny.net dashboard before this
# repository existed: they are adopted into the state on the first apply
# (ids in site.json). Once in the state these blocks do nothing.

import {
  to = bunnynet_storage_zone.this
  id = tostring(local.site.storage_zone_id)
}

import {
  to = bunnynet_pullzone.this
  id = tostring(local.site.pullzone_id)
}

import {
  to = bunnynet_pullzone_hostname.this
  id = "${local.site.pullzone_id}|${local.site.hostname}"
}
