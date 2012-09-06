
import xml.dom.minidom as dom
import cgi
import urllib
import urllib2
import urlparse

try:
    import xml.etree.ElementTree as ElementTree
except:
    import elementtree.ElementTree as ElementTree

import gip_common

log = gip_common.getLogger("GIP.MyOSG")

class MyOSG(object):

    def __init__(self):
        self.resource_groups = []

    def query(self, url):
        urlparts = urlparse.urlsplit(url)
        urlparams = cgi.parse_qsl(urlparts[3])
        urlparams += [("datasource", "summary"),
                      ("summary_attrs_showservice", "on"),
                      ("summary_attrs_showfqdn", "on"),
                      ("summary_attrs_showcontact", "on"),
                      ("summary_attrs_showvoownership", "on"),
                     ]
        params = urllib.urlencode(urlparams, doseq=True)
        urlparts = list(urlparts)
        urlparts[3] = params
        new_url = urlparse.urlunsplit(urlparts)
        log.info("Querying MyOSG URL %s" % new_url)
        fd = urllib2.urlopen(new_url)
        return self.parse(fd)

    def parse(self, fd):
        tree = ElementTree.parse(fd)
        for group in tree.findall("ResourceGroup"):
            info = {}
            info['name'] = group.findtext("GroupName")
            resources = []
            for resource in group.findall("Resources/Resource"):
                info2 = {}
                info2['name'] = resource.findtext("Name")
                info2['fqdn'] = resource.findtext("FQDN")
                services = {}
                for service in resource.findall("Services/Service"):
                    info3 = {}
                    info3['service_uri'] = service.findtext("uri_override")
                    services[service.findtext("Name")] = info3
                ownerships = []
                for ownership in resource.findall("VOOwnership/Ownership"):
                    ownerships.append(ownership.findtext("VO"))
                info2['ownership'] = ownerships
                info2['services'] = services
                resources.append(info2)
            info['resources'] = resources
            self.resource_groups.append(info)

    def getResourceGroups(self):
        return self.resource_groups

