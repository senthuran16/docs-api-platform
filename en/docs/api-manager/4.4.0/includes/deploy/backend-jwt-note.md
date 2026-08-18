---
title: "Backend JWT generator note"
description: "Note on customizing backend JWT claims, since the default generator's claims are subject to change."
canonical_url: https://wso2.com/api-platform/docs/api-manager/4.4.0/includes/deploy/backend-jwt-note/
md_url: https://wso2.com/api-platform/docs/api-manager/4.4.0/includes/deploy/backend-jwt-note.md
tags:
  - api-manager
  - includes
  - deploy
  - backend-jwt-note
author: WSO2 API Platform Documentation Team
last_updated: 2026-07-15
content_type: "concept"
---

!!! note
    WSO2 API Manager comes with the default JWT generator. This JWT generator will generate specific claims based on the specifications and the user demands at the time the product is released. When you update the products, you will need to add/change some of the claims based on the specification updates. This means that even with the given released version, standard claims that come from the API Manager are subjected to change. Therefore, if you have planned to use specific claims in the backend, it is always recommended to implement a custom JWT generator with mandatory claims you wish to consume at your backend.