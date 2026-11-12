// Node.js XML handler rejecting DOCTYPE and ENTITY declarations before parsing.
function run(xml) {
    if (typeof xml !== "string" || xml.length > 1024) return "DENIED";
    if (/<!DOCTYPE|<!ENTITY/i.test(xml)) return "DENIED";
    const match = xml.match(/^<note>([A-Za-z0-9 _-]+)<\/note>$/);
    return match ? match[1] : "DENIED";
}
process.stdout.write(run(process.argv[2]));
