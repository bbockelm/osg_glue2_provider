
import time
import socket

import gip_common
import osg_glue2_provider.myosg as myosg
import osg_glue2_provider.version

log = gip_common.getLogger("GIP.FTS")

default_url = 'http://myosg.grid.iu.edu/rgsummary/xml?all_resources=on&gridtype=on&gridtype_1=on&active=on&active_value=1&disable_value=1&has_wlcg=on'

create_time = time.time()
host = socket.gethostname()

def formatStorage(resource, resource_group):
    info = formatDomain(resource_group)
    info['storage_service_id'] = resource['fqdn']
    return info

def formatSRM(service, resource, resource_group):
    info = formatStorage(resource, resource_group)
    info['srm_endpoint_id'] = "%s/srm/2.2.0" % resource['fqdn']
    info['srm_endpoint_url'] = service.setdefault('uri_override', 'httpg://%s:8443/srm/v2/server' % resource['fqdn'])
    info['srm_service_name'] = info['srm_endpoint_url']
    info['srm_service_endpoint_id'] = "%s_endpoint" % info['srm_endpoint_url']
    return info

def formatSRMPolicy(service, resource, resource_group):
    info = formatSRM(service, resource, resource_group)
    policy_rules = []
    user_domains = []
    for vo in resource['ownership']:
        if vo == "(Other)":
            continue
        vo = vo.lower()
        policy_rules.append("GLUE2PolicyRule: VO:%s" % vo)
        user_domains.append("GLUE2PolicyUserDomainForeignKey: %s" % vo)
    info["vo_policy_rule"] = "\n".join(policy_rules)
    info["user_domain_foreign_key"] = "\n".join(user_domains)
    return info

def formatVOShare(vo, resource, resource_group):
    info = formatStorage(resource, resource_group)
    info['vo'] = vo
    return info

def formatDomain(resource_group):
    info = {}
    info['domain_id'] = resource_group["name"]
    info['domain_description'] = "OSG %s" % resource_group["name"]
    info['info_provider_name'] = "OSG GLUE2 Info provider"
    info['info_provider_version'] = osg_glue2_provider.version.version
    info['info_provider_host'] = host
    info['creation_time'] = create_time
    return info

def main():

    cp = gip_common.config()

    myosg_url = gip_common.cp_get(cp, "MyOSG", "url", default_url)

    MyOSG = myosg.MyOSG()
    MyOSG.query(myosg_url)

    domainTemplate = gip_common.getTemplate("Glue2Site", "GLUE2DomainID")
    groupTemplate = gip_common.getTemplate("Glue2Site", "GLUE2GroupID")
    locationTemplate = gip_common.getTemplate("Glue2Site", "GLUE2LocationID")

    storageServiceTemplate = gip_common.getTemplate("Glue2Storage", "GLUE2ServiceID")
    shareTemplate = gip_common.getTemplate("Glue2Storage", "GLUE2ShareID")
    srmTemplate = gip_common.getTemplate("Glue2Storage", "GLUE2EndpointID")
    srmPolicyTemplate = gip_common.getTemplate("Glue2Storage", "GLUE2PolicyID")

    srmServiceTemplate = gip_common.getTemplate("Glue2Service", "GLUE2ServiceID")
    srmServiceEndpointTemplate = gip_common.getTemplate("Glue2Service", "GLUE2EndpointID")
    srmServicePolicyTemplate = gip_common.getTemplate("Glue2Service", "GLUE2PolicyID")

    for resource_group in MyOSG.getResourceGroups():
        found_srm = False
        for resource in resource_group["resources"]:
            if 'SRMv2' in resource['services'].keys():
                resource_info = formatStorage(resource, resource_group)
                found_srm = True
                gip_common.printTemplate(storageServiceTemplate, resource_info)
                for vo in resource['ownership']:
                    if vo == "(Other)":
                        continue
                    vo = vo.lower()
                    vo_info = formatVOShare(vo, resource, resource_group)
                    gip_common.printTemplate(shareTemplate, vo_info)
                srm_info = formatSRMPolicy(resource['services']['SRMv2'], resource, resource_group)
                gip_common.printTemplate(srmPolicyTemplate, srm_info)
                gip_common.printTemplate(srmTemplate, srm_info)
                gip_common.printTemplate(srmServiceTemplate, srm_info)
                gip_common.printTemplate(srmServiceEndpointTemplate, srm_info)
                gip_common.printTemplate(srmServicePolicyTemplate, srm_info)

        if found_srm: # Only print these once.
            gip_common.printTemplate(domainTemplate, resource_info)
            gip_common.printTemplate(groupTemplate, resource_info)

