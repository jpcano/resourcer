# -*- coding: utf-8 -*-

"""
Module to create the queries
"""

Q_LANGUAGES = """
SELECT Skills.Languages.Name as Language 
FROM [sourced.people_d20160421] 
WHERE Skills.Languages.Name IS NOT NULL
GROUP BY Language 
ORDER BY Language
"""

Q_ECOSYSTEMS = """
SELECT Skills.Ecosystems.Name as Ecosystem 
FROM [sourced.people_d20160421] 
WHERE Skills.Ecosystems.Name IS NOT NULL 
GROUP BY Ecosystem 
ORDER BY Ecosystem
"""

Q_COUNTRIES = """
SELECT Country
FROM [sourced.locations]
GROUP BY Country
ORDER BY Country
"""

Q_SEARCH_LANGUAGES_RELEVANT = """
AND Skills.Languages.IsRelevant
"""

Q_SEARCH_LANGUAGES = """
SUM(IF(Skills.Languages.Name = '{0}' {1}, 1, 0)) WITHIN RECORD as {2},
"""

Q_SEARCH_ECOSYSTEMS = """
SUM(IF(Skills.Ecosystems.Name = '{0}', 1, 0)) WITHIN RECORD as {1},
"""
Q_SEARCH_COUNTRY = """
AND Country IN ({0})
"""
Q_SEARCH_REPORT = """
AND proposal.Report.Text != ''
"""

Q_SEARCH = """
SELECT Email, Country, Report, PageRank, HelpscoutId
FROM (
  SELECT people.Email as Email, 
         Country,
         IF(proposal.Report.Text != '', 'Yes', 'No') as Report,
         PageRank,
         proposal.HelpscoutId as HelpscoutId
  FROM (
   SELECT DefaultEmail.Address as Email,
          Location.Country as Country,
          PageRank,
          {0}
   FROM [sourced.people_d20160421]
  ) people
  INNER JOIN [sourced.proposals] proposal ON proposal.Email = people.Email
  WHERE 
       proposal.Conversation.Length > 1
       {1}
       {2}
       {3}
)
GROUP BY Email, Country, Report, PageRank, HelpscoutId
"""

def createQuery(langs, ecos, countries, report, ANDlangs, ANDecos):
    """
    Creates a raw query for BigQuery

    Args:
        langs: A list of languages. Each element in the list is a list with this
               structure: [string, boolean]. string is a language and boolean points
               if the language is relevant(True) or not(False)
        ecos: A list of strings representing the ecosystems
        countries: A list of strings representing the countries
        report: A boolean that points if we need candidates with report(True) or 
                not(False)
        ANDlangs: A boolean that points if it will apply a AND with the list of
                  languages(True) or not(False)
        ANDecos: A boolean that points if it will apply a AND with the list of
                 ecosystems(True) or not(False)

    Returns:
        A string with the query
    """
    boolLang = 'AND' if ANDlangs else 'OR'
    boolEcos = 'AND' if ANDecos else 'OR'
    langAlias = alias(len(langs), 'L')
    ecoAlias = alias(len(ecos), 'E')

    sumif = sumIfSQL(langs, ecos)
    where = whereSQL(langAlias, boolLang) + whereSQL(ecoAlias, boolEcos)
    whereCountries = countriesSQL(countries)
    report = Q_SEARCH_REPORT if report else ''

    return Q_SEARCH.format(sumif, where, whereCountries, report)
    
def alias(size, prefix):
    """
    Creates a list of alias for the SELECT clauses

    Args:
        size: The number of alias
        prefix: A string to prefix each alias

    Returns:
        A list with the alias
    """
    alias = []
    charNumber = ord('a')
    for _ in range(size):
        alias.append(prefix + chr(charNumber))
        charNumber += 1
    return alias

def sumIfSQL(langs, ecos):
    """
    Creates the SUMIF part of the SELECT clause

    Args:
        langs: A list of languages. Each element in the list is a list with this
        structure: [string, boolean]. string is a language and boolean points
        if the language is relevant(True) or not(False)
        ecos: A list of strings representing the ecosystems

    Returns:
        A string with the SUMIF part
    """
    sumif = []
    charNumber = ord('a')
    for lang in langs:
        langAlias = 'L' + chr(charNumber)
        charNumber += 1
        rel = Q_SEARCH_LANGUAGES_RELEVANT if lang[1] else ''
        sumif.append(Q_SEARCH_LANGUAGES.format(lang[0], rel, langAlias))
    charNumber = ord('a')
    for eco in ecos:
        ecoAlias = 'E' + chr(charNumber)
        charNumber += 1
        sumif.append(Q_SEARCH_ECOSYSTEMS.format(eco, ecoAlias))
    return ''.join(sumif)

def whereSQL(alias, boolType):
    """
    Creates the WHERE part of the query

    Args:
        alias: A list of strings that represents the alias
        boolType: A string that represents the type of boolean to apply to the alias.

    Return:
        A string with the WHERE part
    """
    if len(alias) > 1:
        joinStr = ' > 0 ' + boolType + ' '
        return 'AND (' + joinStr.join(alias) + ' > 0)'
    if len(alias) == 1:
        return 'AND ' + alias[0] + ' > 0 '
    else:
        return ''
    
def countriesSQL(countries):
    """
    Creates the WHERE part for the countries

    Args:
        countries: A list of strings that represents the countries

    Returns:
        A string with the WHERE part
    """
    if countries:
        countriesStr = "'" + "','".join(countries) + "'"
        return Q_SEARCH_COUNTRY.format(countriesStr)
    else:
        return ''
