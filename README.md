# glyphs

## Examples
Sample response JSON from an API call looks as follows. Let's assume for the example that we keep a reference to that dictionary.
```python
my_json_dict = {
    'expand': 'schema,names',
        'issues':[
                    {
                        'expand': 'operations,versionedRepresentations,editmeta,changelog,renderedFields',
                        'fields': {
                            'status': {
                                'description': '',
                                'id': '10001',
                                'name': 'Done',
                                'statusCategory': 
                                            {
                                                'colorName': 'green',
                                                'id': 3,
                                                'key': 'done',
                                                'name': 'Done',
                                            }
                                        }
                                    },
                        'id': '10022',
                        'key': 'XXX-23'},
                     {
                        'expand': 'operations,versionedRepresentations,editmeta,changelog,renderedFields',
                        'fields': {
                            'status': {
                                'description': '',
                                'id': '10001',
                                'name': 'Done',
                                'statusCategory': 
                                            {
                                                'colorName': 'green',
                                                'id': 3,
                                                'key': 'done',
                                                'name': 'Done',
                                            }
                                        }
                                    },
                        'id': '10021',
                        'key': 'XXX-22'},
                     ],
    'maxResults': 50,
    'startAt': 0,
    'total': 17
}
```

How would you get the `status` & `statusCategory`'s `id` for each item of the "issue"?
```python
    issues = my_json_dict['issues']
    
    if issues:
        # add a lot of code to check if the type returns worked for you
        # add a lot of code to handle exceptions

        for issue in issues:
            status_name = issue['fields']['status']['name']
            # add a lot of code to check if the type returned works for you
            # add a lot of code to handle exceptions
            # add a code convert the data or have the rest of your code handle unpredictable returns

            status_id = issue['fields']['status']['statusCategory']['id']
            # add a lot of code to check if the type returned works for you
            # add a lot of code to handle exceptions
            # add a code convert the data or have the rest of your code handle unpredictable returns

```
This is the shortest you could possibly write it. Now you have to hope for the best from there, write a lot of
code to handle exception, data conversion etc.

With Glyphs:
```python
    from glyphs.ro.ROGlyph import ROGlyph
    from glyphs.utils.DictUtils import DictUtils

    issues_glyph = ROGlyph('issues', r_translation_function=list, r_default_value=tuple())
    name_glyph = ROGlyph('fields>status>name', r_translation_function=unicode,)
    cat_id_glyph = ROGlyph('fields>statusCategory>id', r_translation_function=int, r_default_value=-1)

    issues = DictUtils.get(my_json_dict, issues_glyph)
    
    for issue in issues:
        status_name = DictUtils.get(my_json_dict, name_glyph)
        status_id = DictUtils.get(my_json_dict, cat_id_glyph)
```
Similar code with a twist:
1. we know that what we got is precisely what we wanted.
2. simpler errors and missing data are automatically handled for us (with tasteful defaults)
3. it also supports `functools.partial` if we want to make our code shorter
4. the glyphs are infinitely shareable!! reuse and abuse!
5. we can swap `DictUtils` with a different util (any that you want) if the type of `my_json_dict` changes
(in later versions of the code) and everything will still work as we intended.