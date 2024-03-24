# GlotScript Resource

Current Version = V0.1

Check [history](https://github.com/cisnlp/GlotScript/commits/main/metadata/GlotScript.tsv) for other versions. 

## How to load

```python
# ! wget https://raw.githubusercontent.com/cisnlp/GlotScript/main/metadata/GlotScript.tsv
df = pd.read_csv('GlotScript.tsv', na_filter= False, sep='\t')
```

## Format

- MAIN or CORE: Given a language l identified by an ISO639 code, we categorize a script for l as MAIN if
this is supported by at least two of the three sources.

- AUXILIARY (aux): If only one metadata source agrees on a
script and not the other, the script is placed in the
auxiliary category specific to that source. Wiki-aux, LREC2800-aux, and SIL-aux are used for
Wikipedia, LREC_2800, and SIL, respectively.
SIL2-aux is exclusively used for discrepancies between ScriptSource and LangTag.


## License
This dataset is available under the CC BY-SA 4.0 license, permitting modification and redistribution.

## Sources



- [Wikipeida](https://en.wikipedia.org/wiki/ISO_639:xxx): Since Wikipedia writing system metadata is not easily redistributed, we provide our crawled version of the Writing System Text from Wikipedia in the [sources folder](./sources).
- [ScriptSource](https://scriptsource.org/)
- [Unicode CLDR](https://github.com/unicode-org/cldr-json/blob/main/cldr-json/cldr-core/supplemental/likelySubtags.json)
- [LangTag](https://raw.githubusercontent.com/silnrsi/langtags/master/pub/langtags.json)
- [LREC_2800](https://raw.githubusercontent.com/google-research/url-nlp/main/language_metadata/data.tsv)
- [Omniglot](https://www.omniglot.com/writing/langalph.htm)

