<?php
// PHP XML parser resolving external entities via LIBXML_NOENT.
function run(string $xml): string {
    $doc = new DOMDocument();
    if (!@$doc->loadXML($xml, LIBXML_NOENT | LIBXML_DTDLOAD)) {
        return "DENIED";
    }
    return $doc->textContent;
}
echo run($argv[1]);
