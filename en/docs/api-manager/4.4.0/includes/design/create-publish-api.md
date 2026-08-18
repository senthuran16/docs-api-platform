---
title: "Secure the sample API with an API key"
description: "Deploy the sample PizzaShack API in the Publisher and secure it with API key application-level security."
canonical_url: https://wso2.com/api-platform/docs/api-manager/4.4.0/includes/design/create-publish-api/
md_url: https://wso2.com/api-platform/docs/api-manager/4.4.0/includes/design/create-publish-api.md
tags:
  - api-manager
  - includes
  - design
  - create-publish-api
author: WSO2 API Platform Documentation Team
last_updated: 2026-07-15
content_type: "how-to"
---

1. Sign in to the Publisher.  
    
     `https://<hostname>:9443/publisher`

2. Click **DEPLOY SAMPLE API** to deploy the sample PizzaShack API.

3. Click **Develop -> API Configurations -> Runtime** and select **Application Level Security**.

4. Select **API Key**. Note that `APIKey` is used as the default header. This value can be changed using the `APIKey Header` field.

     [![Configure API key authentication](../../../../assets/img/learn/api-key-option.png)](../../../assets/img/learn/api-key-option.png)
     
5. Click **Save and Deploy** to save the changes made within the **Runtime Configurations** page. Upon redirection to the **Deployments** page, select the relevant Gateway and click on **Deploy**.
