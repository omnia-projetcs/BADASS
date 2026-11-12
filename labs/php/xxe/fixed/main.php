<?php
// PHP XML parser rejecting DOCTYPE declarations and disabling entity substitution.
function run(string $xml): string {
    if (stripos($xml, "<!DOCTYPE") !== false || stripos($xml, "<!ENTITY") !== false) {
        return "DENIED";
    }
    $doc = new DOMDocument();
    if (!@$doc->loadXML($xml, LIBXML_NONET)) {
        return "DENIED";
    }
    if ($doc->doctype !== null) {
        return "DENIED";
    }
    return $doc->textContent;
}
echo run($argv[1]);
