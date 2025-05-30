# Lean Data Stack: dbt May Not Be Necessary with Dagster

A colleague and I recently discussed what at first seemed like a question with an obvious answer:

> What **kind** of software is dbt in your data stack?

This colleague's answer was "a transformation tool" to which I rebutted "no, it's an orchestrator". What my research (albeit very shallow) revealed is that my colleague's answer is the widely accepted one. 

Whether it's pride or a rigid pursuit for accuracy, I don't agree with the popular assessment of what the data engineering community dubs the role of dbt in a data stack. So, here's my case. 

## What even is "a transformation tool"?
My conjecture is that dbt itself coined and popularized the term "transformation tool". Before dbt, ETL operations were done usually under a single platform that covered extraction, transformation and loading.

Taking cues from principles that were being applied to software engineering, the developers of dbt thought that a modern data stack would be better served if monolithic ETL tools were split into microservices; the "T" is its chosen niche. In that sense, it goes without saying that transformation is the primary scope of dbt's concern within the data stack. 

This paradigm shift proved to be a huge value add, and now, dbt-like offerings are rearing their heads in troves (e.g. Dataform, Coalesce, SQLMesh). 