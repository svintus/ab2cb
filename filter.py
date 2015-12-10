#!/bin/python


topdomains = [x.strip() for x in open("alexa.txt", "r").readlines()]
topdomains = set(topdomains[:50000])
# topdomains = set(topdomains)


def extract_domains(rule):
    if "##" in rule:
        domains, _ = rule.split("##")
        if len(domains):
            domains = domains.split(",")
            return domains
    
    if "||" in rule:
        domain = rule[2:].split("/")[0].strip("^").split("^")[0].strip('||')
        if len(domain):
            return [domain]

    return []


def alexa_filter(rules):
    keep = []
    discard = []

    for elem in rules:

        domains = extract_domains(elem)
        if not domains:
            keep.append(elem)
            continue
        do_continue = False
        for domain in domains:
            no_subdomain = ".".join(domain.split(".")[-2:])
            if domain in topdomains or no_subdomain in topdomains:
                # print domain + " is in TOP 1000"
                keep.append(elem)
                do_continue = True
                break
        if do_continue:
            continue
        discard.append(elem)

    return keep, discard

