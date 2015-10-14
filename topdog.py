#!/bin/python

topdomains = set([x.strip() for x in open("alexa.txt", "r").readlines()])

elemhide = open("elemhide_sorted.txt", "r").readlines()

# elemhide = elemhide[:100]

keep = []
discard = []

for elem in elemhide:
  domains, elt = elem.split("##")
  domains = domains.split(",")
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


for elem in keep:
  print elem,

# print
# print len(keep), "domains to keep"
# print len(discard), "domains to discard"

