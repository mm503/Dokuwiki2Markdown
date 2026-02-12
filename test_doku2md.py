#!/usr/bin/env python3

import unittest
from doku2md import DokuWiki2MarkDown
from textwrap import dedent


class TestDokuwikiToMarkdown(unittest.TestCase):
    def setUp(self):
        self.dtm = DokuWiki2MarkDown()

    def test_no_timestamp(self):
        self.assertEqual('', self.dtm._rm_timestamp('Created Tuesday 03 April 2012\n'))
        self.assertEqual('', self.dtm._rm_timestamp(' Created Tuesday 03 April 2012\n'))
        self.assertEqual('\n', self.dtm._rm_timestamp('Created Tuesday 03 April 2012\n\n'))
        self.assertEqual('\n\n', self.dtm._rm_timestamp('\nCreated Tuesday 03 April 2012\n\n'))
        self.assertEqual('\n', self.dtm._rm_timestamp('\n'))
        self.assertEqual('Some text\n', self.dtm._rm_timestamp('Some text\n'))
        self.assertEqual(' ', self.dtm._rm_timestamp(' '))

    def test_italic(self):
        self.assertEqual('*italic*', self.dtm._tr_italic('//italic//'))
        self.assertEqual('/not italic//', self.dtm._tr_italic('/not italic//'))
        self.assertEqual('\n *italic*', self.dtm._tr_italic('\n //italic//'))
        self.assertEqual('*italic*\n', self.dtm._tr_italic('//italic//\n'))

    def test_underline(self):
        # Underline (not supported in Markdown, converted to bold)
        self.assertEqual('**underlined**', self.dtm._tr_underline('__underlined__'))
        self.assertEqual('_not_underlined_', self.dtm._tr_underline('_not_underlined_'))
        self.assertEqual('\n **underlined**', self.dtm._tr_underline('\n __underlined__'))
        self.assertEqual('**underlined** \n', self.dtm._tr_underline('__underlined__ \n'))

    def test_monospaced(self):
        self.assertEqual('`monospaced text`', self.dtm._tr_monospaced("''monospaced text''"))
        self.assertEqual('\'not monospaced text\'', self.dtm._tr_monospaced("'not monospaced text'"))
        self.assertEqual('\n `monospaced text`', self.dtm._tr_monospaced("\n ''monospaced text''"))
        self.assertEqual('`monospaced text` \n', self.dtm._tr_monospaced("''monospaced text'' \n"))

    def test_strikethrough(self):
        self.assertEqual('~~strikethrough text~~', self.dtm._tr_strikethrough('<del>strikethrough text</del>'))
        self.assertEqual('<del>not strikethrough text<del>', self.dtm._tr_strikethrough('<del>not strikethrough text<del>'))
        self.assertEqual('\n ~~strikethrough text~~', self.dtm._tr_strikethrough('\n <del>strikethrough text</del>'))
        self.assertEqual('~~strikethrough text~~ \n', self.dtm._tr_strikethrough('<del>strikethrough text</del> \n'))

    def test_links(self):
        self.assertEqual('[Example](https://example.com)\n', self.dtm._dokuwiki_to_markdown('[[https://example.com|Example]]', None, None))
        self.assertEqual('[https://example.com](https://example.com)\n', self.dtm._dokuwiki_to_markdown('[[https://example.com]]', None, None))
        self.assertEqual('[https://example.com//two//slashes](https://example.com//two//slashes)\n', self.dtm._dokuwiki_to_markdown('[[https://example.com//two//slashes]]', None, None))

    def test_headers(self):
        self.assertEqual('# Headline L1\n\n', self.dtm._tr_headers('====== Headline L1 ======\n'))
        self.assertEqual('# Headline L1\n\n', self.dtm._tr_headers('====== Headline L1 ======\n\n'))
        self.assertEqual('# Headline L1\n\n', self.dtm._tr_headers('====== Headline L1 ======\n \n'))
        self.assertEqual('# Headline L1\n\n', self.dtm._tr_headers('====== Headline L1 ======\n \n \n '))
        self.assertEqual('## Headline L2\n\n', self.dtm._tr_headers('===== Headline L2 =====\n'))
        self.assertEqual('### Headline L3\n\n', self.dtm._tr_headers('==== Headline L3 ====\n'))
        self.assertEqual('#### Headline L4\n\n', self.dtm._tr_headers('=== Headline L4 ===\n'))
        self.assertEqual('##### Headline L5\n\n', self.dtm._tr_headers('== Headline L5 ==\n'))
        self.assertEqual('= Not A Headline =\n', self.dtm._tr_headers('= Not A Headline =\n'))

    def test_code_blocks(self):
        self.assertEqual('\n\n```\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<code>\ncode text\n</code>', None, False))
        self.assertEqual('\n\n```\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>\ncode text\n</file>', None, False))
        self.assertEqual('\n\n```\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>code text</file>', None, False))
        self.assertEqual('\n\n```\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>\ncode text</file>', None, False))
        self.assertEqual('\n\n```\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>code text\n</file>', None, False))
        self.assertEqual('\n\n```\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('\n<file>code text\n</file>', None, False))
        # with lang
        self.assertEqual('\n\n```shell\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<code>\ncode text\n</code>', 'shell', False))
        self.assertEqual('\n\n```shell\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>\ncode text\n</file>', 'shell', False))
        self.assertEqual('\n\n```shell\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>code text</file>', 'shell', False))
        self.assertEqual('\n\n```shell\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>\ncode text</file>', 'shell', False))
        self.assertEqual('\n\n```shell\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('<file>code text\n</file>', 'shell', False))
        self.assertEqual('\n\n```shell\ncode text\n```\n\n', self.dtm._dokuwiki_to_markdown('\n<file>code text\n</file>', 'shell', False))

    def test_code_blocks_no_transformation(self):
        # Test that content inside code blocks is not transformed
        # Lists should not be converted
        input_text = '<code>\n  - List item\n  * Another item\n</code>'
        expected = '\n\n```\n  - List item\n  * Another item\n```\n\n'
        result = self.dtm._dokuwiki_to_markdown(input_text, None, False)
        self.assertEqual(expected, result)

        # Italic/bold/underline should not be converted
        input_text2 = '<code>\n//italic//\n**bold**\n__underline__\n</code>'
        expected2 = '\n\n```\n//italic//\n**bold**\n__underline__\n```\n\n'
        result2 = self.dtm._dokuwiki_to_markdown(input_text2, None, False)
        self.assertEqual(expected2, result2)

        # Test that real content outside code blocks is still transformed
        input_text3 = '//italic//\n<code>\n//not italic//\n</code>\n//italic again//'
        expected3 = '*italic*\n\n```\n//not italic//\n```\n\n*italic again*\n'
        result3 = self.dtm._dokuwiki_to_markdown(input_text3, None, False)
        self.assertEqual(expected3, result3)

    def test_images(self):
        self.assertEqual('![alt text](image.png)', self.dtm._tr_images('{{image.png|alt text}}'))

    def test_footnotes(self):
        self.assertEqual('[^1]\n\n[^1]: Footnote text', self.dtm._tr_footnotes('((Footnote text))'))

    def test_linebreaks(self):
        self.assertEqual('Text on line  \n', self.dtm._tr_linebreaks('Text on line \\\\\n'))
        self.assertEqual('Text on line  \n', self.dtm._tr_linebreaks('Text on line \\\\   \n'))
        self.assertEqual('Text on line  \n', self.dtm._tr_linebreaks('Text on line\\\\\n'))
        self.assertEqual('Text on line  \n', self.dtm._tr_linebreaks('Text on line\\\\   \n'))
        self.assertEqual('Text on line  \n', self.dtm._tr_linebreaks('Text on line\\\\ \n'))

    def test_trailing_single_spaces(self):
        self.assertEqual('Text on line\n', self.dtm._rm_single_space_at_line_end('Text on line\n'))
        self.assertEqual('Text on line\n', self.dtm._rm_single_space_at_line_end('Text on line \n'))
        self.assertEqual('Text on line  \n', self.dtm._rm_single_space_at_line_end('Text on line  \n'))
        self.assertEqual('Text on line   \n', self.dtm._rm_single_space_at_line_end('Text on line   \n'))
        self.assertEqual('Text on line    \n', self.dtm._rm_single_space_at_line_end('Text on line    \n'))

    def test_tables(self):
        dw = dedent("""\
        ^ Heading 1      ^ Heading 2       ^ Heading 3          ^
        | Row 1 Col 1    | Row 1 Col 2     | Row 1 Col 3        |
        | Row 2 Col 1    | some colspan (note the double pipe) ||
        | Row 3 Col 1    | Row 3 Col 2     | Row 3 Col 3        |
        """)
        md = dedent("""\
        | Heading 1      | Heading 2       | Heading 3          |
        |  --- | --- | --- |
        | Row 1 Col 1    | Row 1 Col 2     | Row 1 Col 3        |
        | Row 2 Col 1    | some colspan (note the double pipe) | |
        | Row 3 Col 1    | Row 3 Col 2     | Row 3 Col 3        |
        """)
        self.assertEqual(self.dtm._tr_tables(dw), md)

    def test_lists(self):
        self.assertEqual('* Unordered item', self.dtm._tr_lists('  * Unordered item'))
        self.assertEqual('1. Ordered item', self.dtm._tr_lists('  - Ordered item'))
        self.assertEqual('  * Nested unordered item', self.dtm._tr_lists('    * Nested unordered item'))
        self.assertEqual('  1. Nested ordered item', self.dtm._tr_lists('    - Nested ordered item'))
        self.assertEqual('----', self.dtm._tr_lists('----')) # avoid horizontal rule

    def test_lists_counter_reset(self):
        # Test that ordered list counter resets between separate lists
        input_text = '  - First item 1\n  - First item 2\n\n  - Second item 1\n  - Second item 2'
        expected = '1. First item 1\n2. First item 2\n\n1. Second item 1\n2. Second item 2'
        self.assertEqual(expected, self.dtm._tr_lists(input_text))

    def test_newlines(self):
        self.assertEqual('\n', self.dtm._rm_newlines('\n'))
        self.assertEqual('\n\n', self.dtm._rm_newlines('\n\n'))
        self.assertEqual('\n\n', self.dtm._rm_newlines('\n \n\n'))
        self.assertEqual('\n\n', self.dtm._rm_newlines('\n\n\n\n'))
        self.assertEqual('\n\n', self.dtm._rm_newlines('\n  \t  \n'))
        self.assertEqual('\nsometext\n', self.dtm._rm_newlines('\nsometext\n'))
        self.assertEqual('\nsometext\n\n', self.dtm._rm_newlines('\nsometext\n\n'))
        self.assertEqual('\nsometext\n\n', self.dtm._rm_newlines('\nsometext\n\n\n'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
