import json

def get_entities(text):
    import urllib.request
    import urllib.parse
    q_dict = {'lang': 'en', 'gcube-token': '25f9426f-8476-4aae-a512-f364bb8fd9e2-843339462', 'text': text}
    url = "https://tagme.d4science.org/tagme/tag?{0}".format(urllib.parse.urlencode(q_dict))

    json_obj = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    entity_set = set()
    for annotation in json_obj['annotations']:
        entity_set.add(annotation['title'])
    return list(entity_set)

def main():
    text = "Description    A Big Data Developer is required to work with one of the brightest    companies on the European Tech Scene on a range of Visual and    Interaction Design Projects for their hallmark product.  This is an    exciting opportunity to help shape the way in which Data based products    are used by the company in the future and will see you working at the    cutting edge of Big Data in a vibrant,  innovative and stimulating    environment.     Role:    Big Data Developer    As Big Data Developer You Will Be Responsible For    + Developing applications that exploit a unique collection of    scientific data    + Building a cloud based platform that allows easy development of new    applications    + Integrate with wider systems to make data easily available to others    + Work with Product Managers ensure software is high quality and meets    user requirements    As Big Data Developer You Will Have Experience Of    + Degree qualified or equivalent in Computer science or other relevant    discipline    + Development on the JVM using Scala and possibly other JVM languages,     knowledge of Python or R is a bonus    + Experience with Spark,  or the Hadoop ecosystem and similar frameworks    + Familiarity with tools such as AWS,  Mesos or Docker and an instinct    for automation    +Agile experience with Scrum/Kanban/XP    + Experience with agile engineering practices such as TDD,  Pair    Programming,  Continuous Integration,  automated testing and deployment    + Web service development using frameworks such as Dropwizard,     Scalatra,  Hysterix or similar    + A positive,  constructive approach with an emphasis on collaboration    and good execution"

    print(get_entities(text))


if __name__ == '__main__':
    main()
