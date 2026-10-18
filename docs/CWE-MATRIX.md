# Complete CWE coverage matrix

Source: MITRE CWE **4.20**. All **1450** entries from the imported snapshot are included.

**57 implemented weaknesses**, **912 gaps**, **481 category/view entries**.

`implemented` means source pairs and vectors exist, not that a scanner detected them or a runtime was available.
Test results are tracked separately. `gap` is an unimplemented weakness. `taxonomy-only` is a category or view.
Deprecated entries remain visible with their MITRE status. No coverage is inherited from parent categories.

[Machine-readable snapshot](../catalog/cwe.json) · [Attribution and license](../THIRD_PARTY_NOTICES.md)

| CWE | Name | Kind | MITRE status | Coverage | Cases |
|---|---|---|---|---|---|
| CWE-1 | DEPRECATED: Location | category | Deprecated | taxonomy-only |  |
| CWE-2 | 7PK - Environment | category | Draft | taxonomy-only |  |
| CWE-3 | DEPRECATED: Technology-specific Environment Issues | category | Deprecated | taxonomy-only |  |
| CWE-4 | DEPRECATED: J2EE Environment Issues | category | Deprecated | taxonomy-only |  |
| CWE-5 | J2EE Misconfiguration: Data Transmission Without Encryption | weakness | Draft | gap |  |
| CWE-6 | J2EE Misconfiguration: Insufficient Session-ID Length | weakness | Incomplete | gap |  |
| CWE-7 | J2EE Misconfiguration: Missing Custom Error Page | weakness | Incomplete | gap |  |
| CWE-8 | J2EE Misconfiguration: Entity Bean Declared Remote | weakness | Incomplete | gap |  |
| CWE-9 | J2EE Misconfiguration: Weak Access Permissions for EJB Methods | weakness | Draft | gap |  |
| CWE-10 | DEPRECATED: ASP.NET Environment Issues | category | Deprecated | taxonomy-only |  |
| CWE-11 | ASP.NET Misconfiguration: Creating Debug Binary | weakness | Draft | gap |  |
| CWE-12 | ASP.NET Misconfiguration: Missing Custom Error Page | weakness | Draft | gap |  |
| CWE-13 | ASP.NET Misconfiguration: Password in Configuration File | weakness | Draft | gap |  |
| CWE-14 | Compiler Removal of Code to Clear Buffers | weakness | Draft | gap |  |
| CWE-15 | External Control of System or Configuration Setting | weakness | Incomplete | gap |  |
| CWE-16 | Configuration | category | Obsolete | taxonomy-only |  |
| CWE-17 | DEPRECATED: Code | category | Deprecated | taxonomy-only |  |
| CWE-18 | DEPRECATED: Source Code | category | Deprecated | taxonomy-only |  |
| CWE-19 | Data Processing Errors | category | Draft | taxonomy-only |  |
| CWE-20 | Improper Input Validation | weakness | Stable | implemented | [rest-api/unsafe-upstream-data](../labs/rest-api/unsafe-upstream-data/README.md), [ai/training-data-poisoning](../labs/ai/training-data-poisoning/README.md) |
| CWE-21 | DEPRECATED: Pathname Traversal and Equivalence Errors | category | Deprecated | taxonomy-only |  |
| CWE-22 | Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal') | weakness | Stable | implemented | [python/path-traversal](../labs/python/path-traversal/README.md), [node/path-traversal](../labs/node/path-traversal/README.md), [typescript/path-traversal](../labs/typescript/path-traversal/README.md), [php/path-traversal](../labs/php/path-traversal/README.md), [ruby/path-traversal](../labs/ruby/path-traversal/README.md), [go/path-traversal](../labs/go/path-traversal/README.md), [java/path-traversal](../labs/java/path-traversal/README.md), [rust/path-traversal](../labs/rust/path-traversal/README.md), [c/path-traversal](../labs/c/path-traversal/README.md), [cpp/path-traversal](../labs/cpp/path-traversal/README.md), [dotnet/path-traversal](../labs/dotnet/path-traversal/README.md), [cgi/path-traversal](../labs/cgi/path-traversal/README.md), [rest-api/path-traversal](../labs/rest-api/path-traversal/README.md), [ai/path-traversal](../labs/ai/path-traversal/README.md), [python/zip-slip](../labs/python/zip-slip/README.md) |
| CWE-23 | Relative Path Traversal | weakness | Draft | gap |  |
| CWE-24 | Path Traversal: '../filedir' | weakness | Incomplete | gap |  |
| CWE-25 | Path Traversal: '/../filedir' | weakness | Incomplete | gap |  |
| CWE-26 | Path Traversal: '/dir/../filename' | weakness | Draft | gap |  |
| CWE-27 | Path Traversal: 'dir/../../filename' | weakness | Draft | gap |  |
| CWE-28 | Path Traversal: '..\filedir' | weakness | Incomplete | gap |  |
| CWE-29 | Path Traversal: '\..\filename' | weakness | Incomplete | gap |  |
| CWE-30 | Path Traversal: '\dir\..\filename' | weakness | Draft | gap |  |
| CWE-31 | Path Traversal: 'dir\..\..\filename' | weakness | Draft | gap |  |
| CWE-32 | Path Traversal: '...' (Triple Dot) | weakness | Incomplete | gap |  |
| CWE-33 | Path Traversal: '....' (Multiple Dot) | weakness | Incomplete | gap |  |
| CWE-34 | Path Traversal: '....//' | weakness | Incomplete | gap |  |
| CWE-35 | Path Traversal: '.../...//' | weakness | Incomplete | gap |  |
| CWE-36 | Absolute Path Traversal | weakness | Draft | gap |  |
| CWE-37 | Path Traversal: '/absolute/pathname/here' | weakness | Draft | gap |  |
| CWE-38 | Path Traversal: '\absolute\pathname\here' | weakness | Draft | gap |  |
| CWE-39 | Path Traversal: 'C:dirname' | weakness | Draft | gap |  |
| CWE-40 | Path Traversal: '\\UNC\share\name\' (Windows UNC Share) | weakness | Draft | gap |  |
| CWE-41 | Improper Resolution of Path Equivalence | weakness | Incomplete | gap |  |
| CWE-42 | Path Equivalence: 'filename.' (Trailing Dot) | weakness | Incomplete | gap |  |
| CWE-43 | Path Equivalence: 'filename....' (Multiple Trailing Dot) | weakness | Incomplete | gap |  |
| CWE-44 | Path Equivalence: 'file.name' (Internal Dot) | weakness | Incomplete | gap |  |
| CWE-45 | Path Equivalence: 'file...name' (Multiple Internal Dot) | weakness | Incomplete | gap |  |
| CWE-46 | Path Equivalence: 'filename ' (Trailing Space) | weakness | Incomplete | gap |  |
| CWE-47 | Path Equivalence: ' filename' (Leading Space) | weakness | Incomplete | gap |  |
| CWE-48 | Path Equivalence: 'file name' (Internal Whitespace) | weakness | Incomplete | gap |  |
| CWE-49 | Path Equivalence: 'filename/' (Trailing Slash) | weakness | Incomplete | gap |  |
| CWE-50 | Path Equivalence: '//multiple/leading/slash' | weakness | Incomplete | gap |  |
| CWE-51 | Path Equivalence: '/multiple//internal/slash' | weakness | Incomplete | gap |  |
| CWE-52 | Path Equivalence: '/multiple/trailing/slash//' | weakness | Incomplete | gap |  |
| CWE-53 | Path Equivalence: '\multiple\\internal\backslash' | weakness | Incomplete | gap |  |
| CWE-54 | Path Equivalence: 'filedir\' (Trailing Backslash) | weakness | Incomplete | gap |  |
| CWE-55 | Path Equivalence: '/./' (Single Dot Directory) | weakness | Incomplete | gap |  |
| CWE-56 | Path Equivalence: 'filedir*' (Wildcard) | weakness | Incomplete | gap |  |
| CWE-57 | Path Equivalence: 'fakedir/../realdir/filename' | weakness | Incomplete | gap |  |
| CWE-58 | Path Equivalence: Windows 8.3 Filename | weakness | Incomplete | gap |  |
| CWE-59 | Improper Link Resolution Before File Access ('Link Following') | weakness | Draft | implemented | [python/symlink-following](../labs/python/symlink-following/README.md), [cgi/symlink-following](../labs/cgi/symlink-following/README.md), [rest-api/symlink-following](../labs/rest-api/symlink-following/README.md), [ai/symlink-following](../labs/ai/symlink-following/README.md), [c/symlink-following](../labs/c/symlink-following/README.md), [cpp/symlink-following](../labs/cpp/symlink-following/README.md), [node/symlink-following](../labs/node/symlink-following/README.md), [typescript/symlink-following](../labs/typescript/symlink-following/README.md), [php/symlink-following](../labs/php/symlink-following/README.md), [ruby/symlink-following](../labs/ruby/symlink-following/README.md), [go/symlink-following](../labs/go/symlink-following/README.md), [java/symlink-following](../labs/java/symlink-following/README.md), [dotnet/symlink-following](../labs/dotnet/symlink-following/README.md), [rust/symlink-following](../labs/rust/symlink-following/README.md) |
| CWE-60 | DEPRECATED: UNIX Path Link Problems | category | Deprecated | taxonomy-only |  |
| CWE-61 | UNIX Symbolic Link (Symlink) Following | weakness | Incomplete | gap |  |
| CWE-62 | UNIX Hard Link | weakness | Incomplete | gap |  |
| CWE-63 | DEPRECATED: Windows Path Link Problems | category | Deprecated | taxonomy-only |  |
| CWE-64 | Windows Shortcut Following (.LNK) | weakness | Incomplete | gap |  |
| CWE-65 | Windows Hard Link | weakness | Incomplete | gap |  |
| CWE-66 | Improper Handling of File Names that Identify Virtual Resources | weakness | Draft | gap |  |
| CWE-67 | Improper Handling of Windows Device Names | weakness | Incomplete | gap |  |
| CWE-68 | DEPRECATED: Windows Virtual File Problems | category | Deprecated | taxonomy-only |  |
| CWE-69 | Improper Handling of Windows ::DATA Alternate Data Stream | weakness | Incomplete | gap |  |
| CWE-70 | DEPRECATED: Mac Virtual File Problems | category | Deprecated | taxonomy-only |  |
| CWE-71 | DEPRECATED: Apple '.DS_Store' | weakness | Deprecated | gap |  |
| CWE-72 | Improper Handling of Apple HFS+ Alternate Data Stream Path | weakness | Incomplete | gap |  |
| CWE-73 | External Control of File Name or Path | weakness | Draft | gap |  |
| CWE-74 | Improper Neutralization of Special Elements in Output Used by a Downstream Component ('Injection') | weakness | Incomplete | gap |  |
| CWE-75 | Failure to Sanitize Special Elements into a Different Plane (Special Element Injection) | weakness | Draft | gap |  |
| CWE-76 | Improper Neutralization of Equivalent Special Elements | weakness | Draft | gap |  |
| CWE-77 | Improper Neutralization of Special Elements used in a Command ('Command Injection') | weakness | Draft | gap |  |
| CWE-78 | Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection') | weakness | Stable | implemented | [python/command-injection](../labs/python/command-injection/README.md), [node/command-injection](../labs/node/command-injection/README.md), [typescript/command-injection](../labs/typescript/command-injection/README.md), [php/command-injection](../labs/php/command-injection/README.md), [ruby/command-injection](../labs/ruby/command-injection/README.md), [go/command-injection](../labs/go/command-injection/README.md), [java/command-injection](../labs/java/command-injection/README.md), [rust/command-injection](../labs/rust/command-injection/README.md), [c/command-injection](../labs/c/command-injection/README.md), [cpp/command-injection](../labs/cpp/command-injection/README.md), [dotnet/command-injection](../labs/dotnet/command-injection/README.md), [cgi/command-injection](../labs/cgi/command-injection/README.md), [rest-api/command-injection](../labs/rest-api/command-injection/README.md), [ai/command-injection](../labs/ai/command-injection/README.md) |
| CWE-79 | Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting') | weakness | Stable | implemented | [python/xss](../labs/python/xss/README.md), [node/xss](../labs/node/xss/README.md), [typescript/xss](../labs/typescript/xss/README.md), [php/xss](../labs/php/xss/README.md), [ruby/xss](../labs/ruby/xss/README.md), [go/xss](../labs/go/xss/README.md), [java/xss](../labs/java/xss/README.md), [rust/xss](../labs/rust/xss/README.md), [c/xss](../labs/c/xss/README.md), [cpp/xss](../labs/cpp/xss/README.md), [dotnet/xss](../labs/dotnet/xss/README.md), [cgi/xss](../labs/cgi/xss/README.md), [ai/unsafe-model-output](../labs/ai/unsafe-model-output/README.md), [rest-api/xss](../labs/rest-api/xss/README.md), [python/xss-attribute](../labs/python/xss-attribute/README.md) |
| CWE-80 | Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS) | weakness | Incomplete | gap |  |
| CWE-81 | Improper Neutralization of Script in an Error Message Web Page | weakness | Incomplete | gap |  |
| CWE-82 | Improper Neutralization of Script in Attributes of IMG Tags in a Web Page | weakness | Incomplete | gap |  |
| CWE-83 | Improper Neutralization of Script in Attributes in a Web Page | weakness | Draft | gap |  |
| CWE-84 | Improper Neutralization of Encoded URI Schemes in a Web Page | weakness | Draft | gap |  |
| CWE-85 | Doubled Character XSS Manipulations | weakness | Draft | gap |  |
| CWE-86 | Improper Neutralization of Invalid Characters in Identifiers in Web Pages | weakness | Draft | gap |  |
| CWE-87 | Improper Neutralization of Alternate XSS Syntax | weakness | Draft | gap |  |
| CWE-88 | Improper Neutralization of Argument Delimiters in a Command ('Argument Injection') | weakness | Draft | gap |  |
| CWE-89 | Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection') | weakness | Stable | implemented | [python/sql-injection](../labs/python/sql-injection/README.md), [c/sql-injection](../labs/c/sql-injection/README.md), [cpp/sql-injection](../labs/cpp/sql-injection/README.md), [go/sql-injection](../labs/go/sql-injection/README.md), [php/sql-injection](../labs/php/sql-injection/README.md), [node/sql-injection](../labs/node/sql-injection/README.md), [typescript/sql-injection](../labs/typescript/sql-injection/README.md), [java/sql-injection](../labs/java/sql-injection/README.md), [ruby/sql-injection](../labs/ruby/sql-injection/README.md), [dotnet/sql-injection](../labs/dotnet/sql-injection/README.md), [rust/sql-injection](../labs/rust/sql-injection/README.md), [cgi/sql-injection](../labs/cgi/sql-injection/README.md), [rest-api/sql-injection](../labs/rest-api/sql-injection/README.md), [ai/sql-injection](../labs/ai/sql-injection/README.md), [python/sql-order-by](../labs/python/sql-order-by/README.md), [python/sql-second-order](../labs/python/sql-second-order/README.md), [python/sql-login-bypass](../labs/python/sql-login-bypass/README.md) |
| CWE-90 | Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection') | weakness | Draft | gap |  |
| CWE-91 | XML Injection (aka Blind XPath Injection) | weakness | Draft | gap |  |
| CWE-92 | DEPRECATED: Improper Sanitization of Custom Special Characters | weakness | Deprecated | gap |  |
| CWE-93 | Improper Neutralization of CRLF Sequences ('CRLF Injection') | weakness | Draft | gap |  |
| CWE-94 | Improper Control of Generation of Code ('Code Injection') | weakness | Draft | gap |  |
| CWE-95 | Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection') | weakness | Incomplete | implemented | [python/code-injection](../labs/python/code-injection/README.md) |
| CWE-96 | Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection') | weakness | Draft | gap |  |
| CWE-97 | Improper Neutralization of Server-Side Includes (SSI) Within a Web Page | weakness | Draft | gap |  |
| CWE-98 | Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion') | weakness | Draft | gap |  |
| CWE-99 | Improper Control of Resource Identifiers ('Resource Injection') | weakness | Draft | gap |  |
| CWE-100 | DEPRECATED: Technology-Specific Input Validation Problems | category | Deprecated | taxonomy-only |  |
| CWE-101 | DEPRECATED: Struts Validation Problems | category | Deprecated | taxonomy-only |  |
| CWE-102 | Struts: Duplicate Validation Forms | weakness | Incomplete | gap |  |
| CWE-103 | Struts: Incomplete validate() Method Definition | weakness | Draft | gap |  |
| CWE-104 | Struts: Form Bean Does Not Extend Validation Class | weakness | Draft | gap |  |
| CWE-105 | Struts: Form Field Without Validator | weakness | Draft | gap |  |
| CWE-106 | Struts: Plug-in Framework not in Use | weakness | Draft | gap |  |
| CWE-107 | Struts: Unused Validation Form | weakness | Draft | gap |  |
| CWE-108 | Struts: Unvalidated Action Form | weakness | Incomplete | gap |  |
| CWE-109 | Struts: Validator Turned Off | weakness | Draft | gap |  |
| CWE-110 | Struts: Validator Without Form Field | weakness | Draft | gap |  |
| CWE-111 | Direct Use of Unsafe JNI | weakness | Draft | gap |  |
| CWE-112 | Missing XML Validation | weakness | Draft | gap |  |
| CWE-113 | Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Request/Response Splitting') | weakness | Incomplete | implemented | [cgi/header-injection](../labs/cgi/header-injection/README.md), [python/header-injection](../labs/python/header-injection/README.md), [rest-api/header-injection](../labs/rest-api/header-injection/README.md), [ai/header-injection](../labs/ai/header-injection/README.md), [c/header-injection](../labs/c/header-injection/README.md), [cpp/header-injection](../labs/cpp/header-injection/README.md), [node/header-injection](../labs/node/header-injection/README.md), [typescript/header-injection](../labs/typescript/header-injection/README.md), [php/header-injection](../labs/php/header-injection/README.md), [ruby/header-injection](../labs/ruby/header-injection/README.md), [go/header-injection](../labs/go/header-injection/README.md), [java/header-injection](../labs/java/header-injection/README.md), [dotnet/header-injection](../labs/dotnet/header-injection/README.md), [rust/header-injection](../labs/rust/header-injection/README.md) |
| CWE-114 | Process Control | weakness | Incomplete | gap |  |
| CWE-115 | Misinterpretation of Input | weakness | Incomplete | gap |  |
| CWE-116 | Improper Encoding or Escaping of Output | weakness | Draft | gap |  |
| CWE-117 | Improper Output Neutralization for Logs | weakness | Draft | implemented | [python/log-injection](../labs/python/log-injection/README.md), [cgi/log-injection](../labs/cgi/log-injection/README.md), [rest-api/log-injection](../labs/rest-api/log-injection/README.md), [ai/log-injection](../labs/ai/log-injection/README.md), [c/log-injection](../labs/c/log-injection/README.md), [cpp/log-injection](../labs/cpp/log-injection/README.md), [node/log-injection](../labs/node/log-injection/README.md), [typescript/log-injection](../labs/typescript/log-injection/README.md), [php/log-injection](../labs/php/log-injection/README.md), [ruby/log-injection](../labs/ruby/log-injection/README.md), [go/log-injection](../labs/go/log-injection/README.md), [java/log-injection](../labs/java/log-injection/README.md), [dotnet/log-injection](../labs/dotnet/log-injection/README.md), [rust/log-injection](../labs/rust/log-injection/README.md) |
| CWE-118 | Incorrect Access of Indexable Resource ('Range Error') | weakness | Incomplete | gap |  |
| CWE-119 | Improper Restriction of Operations within the Bounds of a Memory Buffer | weakness | Stable | gap |  |
| CWE-120 | Buffer Copy without Checking Size of Input ('Classic Buffer Overflow') | weakness | Incomplete | gap |  |
| CWE-121 | Stack-based Buffer Overflow | weakness | Draft | implemented | [c/stack-buffer-overflow](../labs/c/stack-buffer-overflow/README.md), [cpp/stack-buffer-overflow](../labs/cpp/stack-buffer-overflow/README.md) |
| CWE-122 | Heap-based Buffer Overflow | weakness | Draft | implemented | [c/heap-buffer-overflow](../labs/c/heap-buffer-overflow/README.md), [cpp/heap-buffer-overflow](../labs/cpp/heap-buffer-overflow/README.md) |
| CWE-123 | Write-what-where Condition | weakness | Draft | gap |  |
| CWE-124 | Buffer Underwrite ('Buffer Underflow') | weakness | Incomplete | gap |  |
| CWE-125 | Out-of-bounds Read | weakness | Draft | implemented | [cpp/out-of-bounds-read](../labs/cpp/out-of-bounds-read/README.md), [c/out-of-bounds-read](../labs/c/out-of-bounds-read/README.md) |
| CWE-126 | Buffer Over-read | weakness | Draft | gap |  |
| CWE-127 | Buffer Under-read | weakness | Draft | gap |  |
| CWE-128 | Wrap-around Error | weakness | Incomplete | gap |  |
| CWE-129 | Improper Validation of Array Index | weakness | Draft | gap |  |
| CWE-130 | Improper Handling of Length Parameter Inconsistency | weakness | Incomplete | gap |  |
| CWE-131 | Incorrect Calculation of Buffer Size | weakness | Draft | gap |  |
| CWE-132 | DEPRECATED: Miscalculated Null Termination | weakness | Deprecated | gap |  |
| CWE-133 | String Errors | category | Draft | taxonomy-only |  |
| CWE-134 | Use of Externally-Controlled Format String | weakness | Draft | implemented | [c/format-string](../labs/c/format-string/README.md), [cpp/format-string](../labs/cpp/format-string/README.md) |
| CWE-135 | Incorrect Calculation of Multi-Byte String Length | weakness | Draft | gap |  |
| CWE-136 | Type Errors | category | Draft | taxonomy-only |  |
| CWE-137 | Data Neutralization Issues | category | Draft | taxonomy-only |  |
| CWE-138 | Improper Neutralization of Special Elements | weakness | Draft | gap |  |
| CWE-139 | DEPRECATED: General Special Element Problems | category | Deprecated | taxonomy-only |  |
| CWE-140 | Improper Neutralization of Delimiters | weakness | Draft | gap |  |
| CWE-141 | Improper Neutralization of Parameter/Argument Delimiters | weakness | Draft | gap |  |
| CWE-142 | Improper Neutralization of Value Delimiters | weakness | Draft | gap |  |
| CWE-143 | Improper Neutralization of Record Delimiters | weakness | Draft | gap |  |
| CWE-144 | Improper Neutralization of Line Delimiters | weakness | Draft | gap |  |
| CWE-145 | Improper Neutralization of Section Delimiters | weakness | Incomplete | gap |  |
| CWE-146 | Improper Neutralization of Expression/Command Delimiters | weakness | Incomplete | gap |  |
| CWE-147 | Improper Neutralization of Input Terminators | weakness | Draft | gap |  |
| CWE-148 | Improper Neutralization of Input Leaders | weakness | Draft | gap |  |
| CWE-149 | Improper Neutralization of Quoting Syntax | weakness | Draft | gap |  |
| CWE-150 | Improper Neutralization of Escape, Meta, or Control Sequences | weakness | Incomplete | gap |  |
| CWE-151 | Improper Neutralization of Comment Delimiters | weakness | Draft | gap |  |
| CWE-152 | Improper Neutralization of Macro Symbols | weakness | Draft | gap |  |
| CWE-153 | Improper Neutralization of Substitution Characters | weakness | Draft | gap |  |
| CWE-154 | Improper Neutralization of Variable Name Delimiters | weakness | Incomplete | gap |  |
| CWE-155 | Improper Neutralization of Wildcards or Matching Symbols | weakness | Draft | gap |  |
| CWE-156 | Improper Neutralization of Whitespace | weakness | Draft | gap |  |
| CWE-157 | Failure to Sanitize Paired Delimiters | weakness | Draft | gap |  |
| CWE-158 | Improper Neutralization of Null Byte or NUL Character | weakness | Incomplete | gap |  |
| CWE-159 | Improper Handling of Invalid Use of Special Elements | weakness | Draft | gap |  |
| CWE-160 | Improper Neutralization of Leading Special Elements | weakness | Incomplete | gap |  |
| CWE-161 | Improper Neutralization of Multiple Leading Special Elements | weakness | Incomplete | gap |  |
| CWE-162 | Improper Neutralization of Trailing Special Elements | weakness | Incomplete | gap |  |
| CWE-163 | Improper Neutralization of Multiple Trailing Special Elements | weakness | Incomplete | gap |  |
| CWE-164 | Improper Neutralization of Internal Special Elements | weakness | Incomplete | gap |  |
| CWE-165 | Improper Neutralization of Multiple Internal Special Elements | weakness | Incomplete | gap |  |
| CWE-166 | Improper Handling of Missing Special Element | weakness | Draft | gap |  |
| CWE-167 | Improper Handling of Additional Special Element | weakness | Draft | gap |  |
| CWE-168 | Improper Handling of Inconsistent Special Elements | weakness | Draft | gap |  |
| CWE-169 | DEPRECATED: Technology-Specific Special Elements | category | Deprecated | taxonomy-only |  |
| CWE-170 | Improper Null Termination | weakness | Incomplete | gap |  |
| CWE-171 | DEPRECATED: Cleansing, Canonicalization, and Comparison Errors | category | Deprecated | taxonomy-only |  |
| CWE-172 | Encoding Error | weakness | Draft | gap |  |
| CWE-173 | Improper Handling of Alternate Encoding | weakness | Draft | gap |  |
| CWE-174 | Double Decoding of the Same Data | weakness | Draft | gap |  |
| CWE-175 | Improper Handling of Mixed Encoding | weakness | Draft | gap |  |
| CWE-176 | Improper Handling of Unicode Encoding | weakness | Draft | gap |  |
| CWE-177 | Improper Handling of URL Encoding (Hex Encoding) | weakness | Draft | gap |  |
| CWE-178 | Improper Handling of Case Sensitivity | weakness | Incomplete | gap |  |
| CWE-179 | Incorrect Behavior Order: Early Validation | weakness | Incomplete | gap |  |
| CWE-180 | Incorrect Behavior Order: Validate Before Canonicalize | weakness | Draft | gap |  |
| CWE-181 | Incorrect Behavior Order: Validate Before Filter | weakness | Draft | gap |  |
| CWE-182 | Collapse of Data into Unsafe Value | weakness | Draft | gap |  |
| CWE-183 | Permissive List of Allowed Inputs | weakness | Draft | gap |  |
| CWE-184 | Incomplete List of Disallowed Inputs | weakness | Draft | gap |  |
| CWE-185 | Incorrect Regular Expression | weakness | Draft | gap |  |
| CWE-186 | Overly Restrictive Regular Expression | weakness | Draft | gap |  |
| CWE-187 | Partial String Comparison | weakness | Incomplete | gap |  |
| CWE-188 | Reliance on Data/Memory Layout | weakness | Draft | gap |  |
| CWE-189 | Numeric Errors | category | Draft | taxonomy-only |  |
| CWE-190 | Integer Overflow or Wraparound | weakness | Stable | implemented | [rust/integer-overflow](../labs/rust/integer-overflow/README.md), [c/integer-overflow](../labs/c/integer-overflow/README.md), [cpp/integer-overflow](../labs/cpp/integer-overflow/README.md) |
| CWE-191 | Integer Underflow (Wrap or Wraparound) | weakness | Draft | gap |  |
| CWE-192 | Integer Coercion Error | weakness | Incomplete | gap |  |
| CWE-193 | Off-by-one Error | weakness | Draft | gap |  |
| CWE-194 | Unexpected Sign Extension | weakness | Incomplete | gap |  |
| CWE-195 | Signed to Unsigned Conversion Error | weakness | Draft | gap |  |
| CWE-196 | Unsigned to Signed Conversion Error | weakness | Draft | gap |  |
| CWE-197 | Numeric Truncation Error | weakness | Incomplete | gap |  |
| CWE-198 | Use of Incorrect Byte Ordering | weakness | Draft | gap |  |
| CWE-199 | Information Management Errors | category | Draft | taxonomy-only |  |
| CWE-200 | Exposure of Sensitive Information to an Unauthorized Actor | weakness | Draft | implemented | [ai/sensitive-context](../labs/ai/sensitive-context/README.md), [ai/system-prompt-leakage](../labs/ai/system-prompt-leakage/README.md) |
| CWE-201 | Insertion of Sensitive Information Into Sent Data | weakness | Draft | gap |  |
| CWE-202 | Exposure of Sensitive Information Through Data Queries | weakness | Draft | gap |  |
| CWE-203 | Observable Discrepancy | weakness | Incomplete | gap |  |
| CWE-204 | Observable Response Discrepancy | weakness | Incomplete | gap |  |
| CWE-205 | Observable Behavioral Discrepancy | weakness | Incomplete | gap |  |
| CWE-206 | Observable Internal Behavioral Discrepancy | weakness | Incomplete | gap |  |
| CWE-207 | Observable Behavioral Discrepancy With Equivalent Products | weakness | Draft | gap |  |
| CWE-208 | Observable Timing Discrepancy | weakness | Incomplete | gap |  |
| CWE-209 | Generation of Error Message Containing Sensitive Information | weakness | Draft | implemented | [python/error-disclosure](../labs/python/error-disclosure/README.md), [cgi/error-disclosure](../labs/cgi/error-disclosure/README.md), [rest-api/error-disclosure](../labs/rest-api/error-disclosure/README.md), [ai/error-disclosure](../labs/ai/error-disclosure/README.md), [c/error-disclosure](../labs/c/error-disclosure/README.md), [cpp/error-disclosure](../labs/cpp/error-disclosure/README.md), [node/error-disclosure](../labs/node/error-disclosure/README.md), [typescript/error-disclosure](../labs/typescript/error-disclosure/README.md), [php/error-disclosure](../labs/php/error-disclosure/README.md), [ruby/error-disclosure](../labs/ruby/error-disclosure/README.md), [go/error-disclosure](../labs/go/error-disclosure/README.md), [java/error-disclosure](../labs/java/error-disclosure/README.md), [dotnet/error-disclosure](../labs/dotnet/error-disclosure/README.md), [rust/error-disclosure](../labs/rust/error-disclosure/README.md) |
| CWE-210 | Self-generated Error Message Containing Sensitive Information | weakness | Draft | gap |  |
| CWE-211 | Externally-Generated Error Message Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-212 | Improper Removal of Sensitive Information Before Storage or Transfer | weakness | Incomplete | gap |  |
| CWE-213 | Exposure of Sensitive Information Due to Incompatible Policies | weakness | Draft | gap |  |
| CWE-214 | Invocation of Process Using Visible Sensitive Information | weakness | Incomplete | gap |  |
| CWE-215 | Insertion of Sensitive Information Into Debugging Code | weakness | Draft | gap |  |
| CWE-216 | DEPRECATED: Containment Errors (Container Errors) | weakness | Deprecated | gap |  |
| CWE-217 | DEPRECATED: Failure to Protect Stored Data from Modification | weakness | Deprecated | gap |  |
| CWE-218 | DEPRECATED: Failure to provide confidentiality for stored data | weakness | Deprecated | gap |  |
| CWE-219 | Storage of File with Sensitive Data Under Web Root | weakness | Draft | gap |  |
| CWE-220 | Storage of File With Sensitive Data Under FTP Root | weakness | Draft | gap |  |
| CWE-221 | Information Loss or Omission | weakness | Incomplete | gap |  |
| CWE-222 | Truncation of Security-relevant Information | weakness | Draft | gap |  |
| CWE-223 | Omission of Security-relevant Information | weakness | Draft | gap |  |
| CWE-224 | Obscured Security-relevant Information by Alternate Name | weakness | Incomplete | gap |  |
| CWE-225 | DEPRECATED: General Information Management Problems | weakness | Deprecated | gap |  |
| CWE-226 | Sensitive Information in Resource Not Removed Before Reuse | weakness | Draft | gap |  |
| CWE-227 | 7PK - API Abuse | category | Draft | taxonomy-only |  |
| CWE-228 | Improper Handling of Syntactically Invalid Structure | weakness | Incomplete | gap |  |
| CWE-229 | Improper Handling of Values | weakness | Incomplete | gap |  |
| CWE-230 | Improper Handling of Missing Values | weakness | Draft | gap |  |
| CWE-231 | Improper Handling of Extra Values | weakness | Draft | gap |  |
| CWE-232 | Improper Handling of Undefined Values | weakness | Draft | gap |  |
| CWE-233 | Improper Handling of Parameters | weakness | Incomplete | gap |  |
| CWE-234 | Failure to Handle Missing Parameter | weakness | Incomplete | gap |  |
| CWE-235 | Improper Handling of Extra Parameters | weakness | Draft | gap |  |
| CWE-236 | Improper Handling of Undefined Parameters | weakness | Draft | gap |  |
| CWE-237 | Improper Handling of Structural Elements | weakness | Incomplete | gap |  |
| CWE-238 | Improper Handling of Incomplete Structural Elements | weakness | Draft | gap |  |
| CWE-239 | Failure to Handle Incomplete Element | weakness | Draft | gap |  |
| CWE-240 | Improper Handling of Inconsistent Structural Elements | weakness | Draft | gap |  |
| CWE-241 | Improper Handling of Unexpected Data Type | weakness | Draft | gap |  |
| CWE-242 | Use of Inherently Dangerous Function | weakness | Draft | gap |  |
| CWE-243 | Creation of chroot Jail Without Changing Working Directory | weakness | Draft | gap |  |
| CWE-244 | Improper Clearing of Heap Memory Before Release ('Heap Inspection') | weakness | Draft | gap |  |
| CWE-245 | J2EE Bad Practices: Direct Management of Connections | weakness | Draft | gap |  |
| CWE-246 | J2EE Bad Practices: Direct Use of Sockets | weakness | Draft | gap |  |
| CWE-247 | DEPRECATED: Reliance on DNS Lookups in a Security Decision | weakness | Deprecated | gap |  |
| CWE-248 | Uncaught Exception | weakness | Draft | gap |  |
| CWE-249 | DEPRECATED: Often Misused: Path Manipulation | weakness | Deprecated | gap |  |
| CWE-250 | Execution with Unnecessary Privileges | weakness | Draft | gap |  |
| CWE-251 | Often Misused: String Management | category | Incomplete | taxonomy-only |  |
| CWE-252 | Unchecked Return Value | weakness | Draft | gap |  |
| CWE-253 | Incorrect Check of Function Return Value | weakness | Incomplete | gap |  |
| CWE-254 | 7PK - Security Features | category | Incomplete | taxonomy-only |  |
| CWE-255 | Credentials Management Errors | category | Draft | taxonomy-only |  |
| CWE-256 | Plaintext Storage of a Password | weakness | Incomplete | gap |  |
| CWE-257 | Storing Passwords in a Recoverable Format | weakness | Incomplete | gap |  |
| CWE-258 | Empty Password in Configuration File | weakness | Incomplete | gap |  |
| CWE-259 | Use of Hard-coded Password | weakness | Draft | gap |  |
| CWE-260 | Password in Configuration File | weakness | Incomplete | gap |  |
| CWE-261 | Weak Encoding for Password | weakness | Incomplete | gap |  |
| CWE-262 | Not Using Password Aging | weakness | Draft | gap |  |
| CWE-263 | Password Aging with Long Expiration | weakness | Draft | gap |  |
| CWE-264 | Permissions, Privileges, and Access Controls | category | Obsolete | taxonomy-only |  |
| CWE-265 | Privilege Issues | category | Incomplete | taxonomy-only |  |
| CWE-266 | Incorrect Privilege Assignment | weakness | Draft | gap |  |
| CWE-267 | Privilege Defined With Unsafe Actions | weakness | Incomplete | gap |  |
| CWE-268 | Privilege Chaining | weakness | Draft | gap |  |
| CWE-269 | Improper Privilege Management | weakness | Draft | gap |  |
| CWE-270 | Privilege Context Switching Error | weakness | Draft | gap |  |
| CWE-271 | Privilege Dropping / Lowering Errors | weakness | Incomplete | gap |  |
| CWE-272 | Least Privilege Violation | weakness | Incomplete | gap |  |
| CWE-273 | Improper Check for Dropped Privileges | weakness | Incomplete | gap |  |
| CWE-274 | Improper Handling of Insufficient Privileges | weakness | Draft | gap |  |
| CWE-275 | Permission Issues | category | Draft | taxonomy-only |  |
| CWE-276 | Incorrect Default Permissions | weakness | Draft | gap |  |
| CWE-277 | Insecure Inherited Permissions | weakness | Draft | gap |  |
| CWE-278 | Insecure Preserved Inherited Permissions | weakness | Incomplete | gap |  |
| CWE-279 | Incorrect Execution-Assigned Permissions | weakness | Draft | gap |  |
| CWE-280 | Improper Handling of Insufficient Permissions or Privileges | weakness | Draft | gap |  |
| CWE-281 | Improper Preservation of Permissions | weakness | Draft | gap |  |
| CWE-282 | Improper Ownership Management | weakness | Draft | gap |  |
| CWE-283 | Unverified Ownership | weakness | Draft | gap |  |
| CWE-284 | Improper Access Control | weakness | Incomplete | gap |  |
| CWE-285 | Improper Authorization | weakness | Draft | gap |  |
| CWE-286 | Incorrect User Management | weakness | Incomplete | gap |  |
| CWE-287 | Improper Authentication | weakness | Draft | implemented | [rest-api/broken-authentication](../labs/rest-api/broken-authentication/README.md) |
| CWE-288 | Authentication Bypass Using an Alternate Path or Channel | weakness | Incomplete | gap |  |
| CWE-289 | Authentication Bypass by Alternate Name | weakness | Incomplete | gap |  |
| CWE-290 | Authentication Bypass by Spoofing | weakness | Incomplete | gap |  |
| CWE-291 | Reliance on IP Address for Authentication | weakness | Incomplete | gap |  |
| CWE-292 | DEPRECATED: Trusting Self-reported DNS Name | weakness | Deprecated | gap |  |
| CWE-293 | Using Referer Field for Authentication | weakness | Draft | gap |  |
| CWE-294 | Authentication Bypass by Capture-replay | weakness | Incomplete | gap |  |
| CWE-295 | Improper Certificate Validation | weakness | Draft | implemented | [python/tls-verification](../labs/python/tls-verification/README.md) |
| CWE-296 | Improper Following of a Certificate's Chain of Trust | weakness | Draft | gap |  |
| CWE-297 | Improper Validation of Certificate with Host Mismatch | weakness | Incomplete | gap |  |
| CWE-298 | Improper Validation of Certificate Expiration | weakness | Draft | gap |  |
| CWE-299 | Improper Check for Certificate Revocation | weakness | Draft | gap |  |
| CWE-300 | Channel Accessible by Non-Endpoint | weakness | Draft | gap |  |
| CWE-301 | Reflection Attack in an Authentication Protocol | weakness | Draft | gap |  |
| CWE-302 | Authentication Bypass by Assumed-Immutable Data | weakness | Incomplete | gap |  |
| CWE-303 | Incorrect Implementation of Authentication Algorithm | weakness | Draft | gap |  |
| CWE-304 | Missing Critical Step in Authentication | weakness | Draft | gap |  |
| CWE-305 | Authentication Bypass by Primary Weakness | weakness | Draft | gap |  |
| CWE-306 | Missing Authentication for Critical Function | weakness | Draft | gap |  |
| CWE-307 | Improper Restriction of Excessive Authentication Attempts | weakness | Draft | gap |  |
| CWE-308 | Use of Single-factor Authentication | weakness | Draft | gap |  |
| CWE-309 | Use of Password System for Primary Authentication | weakness | Draft | gap |  |
| CWE-310 | Cryptographic Issues | category | Draft | taxonomy-only |  |
| CWE-311 | Missing Encryption of Sensitive Data | weakness | Draft | gap |  |
| CWE-312 | Cleartext Storage of Sensitive Information | weakness | Draft | gap |  |
| CWE-313 | Cleartext Storage in a File or on Disk | weakness | Draft | gap |  |
| CWE-314 | Cleartext Storage in the Registry | weakness | Draft | gap |  |
| CWE-315 | Cleartext Storage of Sensitive Information in a Cookie | weakness | Draft | gap |  |
| CWE-316 | Cleartext Storage of Sensitive Information in Memory | weakness | Draft | gap |  |
| CWE-317 | Cleartext Storage of Sensitive Information in GUI | weakness | Draft | gap |  |
| CWE-318 | Cleartext Storage of Sensitive Information in Executable | weakness | Draft | gap |  |
| CWE-319 | Cleartext Transmission of Sensitive Information | weakness | Draft | gap |  |
| CWE-320 | Key Management Errors | category | Obsolete | taxonomy-only |  |
| CWE-321 | Use of Hard-coded Cryptographic Key | weakness | Draft | implemented | [python/jwt-default-key](../labs/python/jwt-default-key/README.md) |
| CWE-322 | Key Exchange without Entity Authentication | weakness | Draft | gap |  |
| CWE-323 | Reusing a Nonce, Key Pair in Encryption | weakness | Incomplete | gap |  |
| CWE-324 | Use of a Key Past its Expiration Date | weakness | Draft | gap |  |
| CWE-325 | Missing Cryptographic Step | weakness | Draft | gap |  |
| CWE-326 | Inadequate Encryption Strength | weakness | Draft | gap |  |
| CWE-327 | Use of a Broken or Risky Cryptographic Algorithm | weakness | Draft | gap |  |
| CWE-328 | Use of Weak Hash | weakness | Draft | gap |  |
| CWE-329 | Generation of Predictable IV with CBC Mode | weakness | Draft | gap |  |
| CWE-330 | Use of Insufficiently Random Values | weakness | Stable | implemented | [python/predictable-token](../labs/python/predictable-token/README.md) |
| CWE-331 | Insufficient Entropy | weakness | Draft | gap |  |
| CWE-332 | Insufficient Entropy in PRNG | weakness | Draft | gap |  |
| CWE-333 | Improper Handling of Insufficient Entropy in TRNG | weakness | Draft | gap |  |
| CWE-334 | Small Space of Random Values | weakness | Draft | gap |  |
| CWE-335 | Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG) | weakness | Draft | gap |  |
| CWE-336 | Same Seed in Pseudo-Random Number Generator (PRNG) | weakness | Draft | gap |  |
| CWE-337 | Predictable Seed in Pseudo-Random Number Generator (PRNG) | weakness | Draft | gap |  |
| CWE-338 | Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG) | weakness | Draft | gap |  |
| CWE-339 | Small Seed Space in PRNG | weakness | Draft | gap |  |
| CWE-340 | Generation of Predictable Numbers or Identifiers | weakness | Incomplete | gap |  |
| CWE-341 | Predictable from Observable State | weakness | Draft | gap |  |
| CWE-342 | Predictable Exact Value from Previous Values | weakness | Draft | gap |  |
| CWE-343 | Predictable Value Range from Previous Values | weakness | Draft | gap |  |
| CWE-344 | Use of Invariant Value in Dynamically Changing Context | weakness | Draft | gap |  |
| CWE-345 | Insufficient Verification of Data Authenticity | weakness | Draft | implemented | [ai/unverified-security-claim](../labs/ai/unverified-security-claim/README.md) |
| CWE-346 | Origin Validation Error | weakness | Draft | implemented | [python/password-reset-host](../labs/python/password-reset-host/README.md) |
| CWE-347 | Improper Verification of Cryptographic Signature | weakness | Draft | gap |  |
| CWE-348 | Use of Less Trusted Source | weakness | Draft | gap |  |
| CWE-349 | Acceptance of Extraneous Untrusted Data With Trusted Data | weakness | Draft | gap |  |
| CWE-350 | Reliance on Reverse DNS Resolution for a Security-Critical Action | weakness | Draft | gap |  |
| CWE-351 | Insufficient Type Distinction | weakness | Draft | gap |  |
| CWE-352 | Cross-Site Request Forgery (CSRF) | weakness | Stable | implemented | [python/csrf](../labs/python/csrf/README.md) |
| CWE-353 | Missing Support for Integrity Check | weakness | Draft | gap |  |
| CWE-354 | Improper Validation of Integrity Check Value | weakness | Draft | gap |  |
| CWE-355 | User Interface Security Issues | category | Draft | taxonomy-only |  |
| CWE-356 | Product UI does not Warn User of Unsafe Actions | weakness | Incomplete | gap |  |
| CWE-357 | Insufficient UI Warning of Dangerous Operations | weakness | Draft | gap |  |
| CWE-358 | Improperly Implemented Security Check for Standard | weakness | Draft | gap |  |
| CWE-359 | Exposure of Private Personal Information to an Unauthorized Actor | weakness | Incomplete | gap |  |
| CWE-360 | Trust of System Event Data | weakness | Incomplete | gap |  |
| CWE-361 | 7PK - Time and State | category | Incomplete | taxonomy-only |  |
| CWE-362 | Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition') | weakness | Draft | implemented | [rest-api/order-concurrency](../labs/rest-api/order-concurrency/README.md) |
| CWE-363 | Race Condition Enabling Link Following | weakness | Draft | gap |  |
| CWE-364 | Signal Handler Race Condition | weakness | Incomplete | gap |  |
| CWE-365 | DEPRECATED: Race Condition in Switch | weakness | Deprecated | gap |  |
| CWE-366 | Race Condition within a Thread | weakness | Draft | gap |  |
| CWE-367 | Time-of-check Time-of-use (TOCTOU) Race Condition | weakness | Incomplete | gap |  |
| CWE-368 | Context Switching Race Condition | weakness | Draft | gap |  |
| CWE-369 | Divide By Zero | weakness | Draft | gap |  |
| CWE-370 | Missing Check for Certificate Revocation after Initial Check | weakness | Draft | gap |  |
| CWE-371 | State Issues | category | Draft | taxonomy-only |  |
| CWE-372 | Incomplete Internal State Distinction | weakness | Draft | gap |  |
| CWE-373 | DEPRECATED: State Synchronization Error | weakness | Deprecated | gap |  |
| CWE-374 | Passing Mutable Objects to an Untrusted Method | weakness | Draft | gap |  |
| CWE-375 | Returning a Mutable Object to an Untrusted Caller | weakness | Draft | gap |  |
| CWE-376 | DEPRECATED: Temporary File Issues | category | Deprecated | taxonomy-only |  |
| CWE-377 | Insecure Temporary File | weakness | Incomplete | gap |  |
| CWE-378 | Creation of Temporary File With Insecure Permissions | weakness | Draft | gap |  |
| CWE-379 | Creation of Temporary File in Directory with Insecure Permissions | weakness | Incomplete | gap |  |
| CWE-380 | DEPRECATED: Technology-Specific Time and State Issues | category | Deprecated | taxonomy-only |  |
| CWE-381 | DEPRECATED: J2EE Time and State Issues | category | Deprecated | taxonomy-only |  |
| CWE-382 | J2EE Bad Practices: Use of System.exit() | weakness | Draft | gap |  |
| CWE-383 | J2EE Bad Practices: Direct Use of Threads | weakness | Draft | gap |  |
| CWE-384 | Session Fixation | weakness | Incomplete | implemented | [python/session-fixation](../labs/python/session-fixation/README.md) |
| CWE-385 | Covert Timing Channel | weakness | Incomplete | gap |  |
| CWE-386 | Symbolic Name not Mapping to Correct Object | weakness | Draft | gap |  |
| CWE-387 | Signal Errors | category | Incomplete | taxonomy-only |  |
| CWE-388 | 7PK - Errors | category | Draft | taxonomy-only |  |
| CWE-389 | Error Conditions, Return Values, Status Codes | category | Incomplete | taxonomy-only |  |
| CWE-390 | Detection of Error Condition Without Action | weakness | Draft | gap |  |
| CWE-391 | Unchecked Error Condition | weakness | Incomplete | gap |  |
| CWE-392 | Missing Report of Error Condition | weakness | Draft | gap |  |
| CWE-393 | Return of Wrong Status Code | weakness | Draft | gap |  |
| CWE-394 | Unexpected Status Code or Return Value | weakness | Draft | gap |  |
| CWE-395 | Use of NullPointerException Catch to Detect NULL Pointer Dereference | weakness | Draft | gap |  |
| CWE-396 | Declaration of Catch for Generic Exception | weakness | Draft | gap |  |
| CWE-397 | Declaration of Throws for Generic Exception | weakness | Draft | gap |  |
| CWE-398 | 7PK - Code Quality | category | Draft | taxonomy-only |  |
| CWE-399 | Resource Management Errors | category | Draft | taxonomy-only |  |
| CWE-400 | Uncontrolled Resource Consumption | weakness | Draft | implemented | [python/unbounded-work](../labs/python/unbounded-work/README.md), [cgi/unbounded-work](../labs/cgi/unbounded-work/README.md), [rest-api/unbounded-work](../labs/rest-api/unbounded-work/README.md), [ai/unbounded-work](../labs/ai/unbounded-work/README.md), [c/unbounded-work](../labs/c/unbounded-work/README.md), [cpp/unbounded-work](../labs/cpp/unbounded-work/README.md), [node/unbounded-work](../labs/node/unbounded-work/README.md), [typescript/unbounded-work](../labs/typescript/unbounded-work/README.md), [php/unbounded-work](../labs/php/unbounded-work/README.md), [ruby/unbounded-work](../labs/ruby/unbounded-work/README.md), [go/unbounded-work](../labs/go/unbounded-work/README.md), [java/unbounded-work](../labs/java/unbounded-work/README.md), [dotnet/unbounded-work](../labs/dotnet/unbounded-work/README.md), [rust/unbounded-work](../labs/rust/unbounded-work/README.md) |
| CWE-401 | Missing Release of Memory after Effective Lifetime | weakness | Draft | gap |  |
| CWE-402 | Transmission of Private Resources into a New Sphere ('Resource Leak') | weakness | Draft | gap |  |
| CWE-403 | Exposure of File Descriptor to Unintended Control Sphere ('File Descriptor Leak') | weakness | Draft | gap |  |
| CWE-404 | Improper Resource Shutdown or Release | weakness | Draft | gap |  |
| CWE-405 | Asymmetric Resource Consumption (Amplification) | weakness | Incomplete | gap |  |
| CWE-406 | Insufficient Control of Network Message Volume (Network Amplification) | weakness | Incomplete | gap |  |
| CWE-407 | Inefficient Algorithmic Complexity | weakness | Incomplete | gap |  |
| CWE-408 | Incorrect Behavior Order: Early Amplification | weakness | Draft | gap |  |
| CWE-409 | Improper Handling of Highly Compressed Data (Data Amplification) | weakness | Incomplete | gap |  |
| CWE-410 | Insufficient Resource Pool | weakness | Incomplete | gap |  |
| CWE-411 | Resource Locking Problems | category | Draft | taxonomy-only |  |
| CWE-412 | Unrestricted Externally Accessible Lock | weakness | Incomplete | gap |  |
| CWE-413 | Improper Resource Locking | weakness | Draft | gap |  |
| CWE-414 | Missing Lock Check | weakness | Draft | gap |  |
| CWE-415 | Double Free | weakness | Draft | implemented | [c/double-free](../labs/c/double-free/README.md), [cpp/double-free](../labs/cpp/double-free/README.md) |
| CWE-416 | Use After Free | weakness | Stable | implemented | [c/use-after-free](../labs/c/use-after-free/README.md), [cpp/use-after-free](../labs/cpp/use-after-free/README.md) |
| CWE-417 | Communication Channel Errors | category | Draft | taxonomy-only |  |
| CWE-418 | DEPRECATED: Channel Errors | category | Deprecated | taxonomy-only |  |
| CWE-419 | Unprotected Primary Channel | weakness | Draft | gap |  |
| CWE-420 | Unprotected Alternate Channel | weakness | Draft | gap |  |
| CWE-421 | Race Condition During Access to Alternate Channel | weakness | Draft | gap |  |
| CWE-422 | Unprotected Windows Messaging Channel ('Shatter') | weakness | Draft | gap |  |
| CWE-423 | DEPRECATED: Proxied Trusted Channel | weakness | Deprecated | gap |  |
| CWE-424 | Improper Protection of Alternate Path | weakness | Draft | gap |  |
| CWE-425 | Direct Request ('Forced Browsing') | weakness | Incomplete | gap |  |
| CWE-426 | Untrusted Search Path | weakness | Stable | gap |  |
| CWE-427 | Uncontrolled Search Path Element | weakness | Draft | gap |  |
| CWE-428 | Unquoted Search Path or Element | weakness | Draft | gap |  |
| CWE-429 | Handler Errors | category | Draft | taxonomy-only |  |
| CWE-430 | Deployment of Wrong Handler | weakness | Incomplete | gap |  |
| CWE-431 | Missing Handler | weakness | Draft | gap |  |
| CWE-432 | Dangerous Signal Handler not Disabled During Sensitive Operations | weakness | Draft | gap |  |
| CWE-433 | Unparsed Raw Web Content Delivery | weakness | Incomplete | gap |  |
| CWE-434 | Unrestricted Upload of File with Dangerous Type | weakness | Draft | implemented | [python/unrestricted-upload](../labs/python/unrestricted-upload/README.md) |
| CWE-435 | Improper Interaction Between Multiple Correctly-Behaving Entities | weakness | Draft | gap |  |
| CWE-436 | Interpretation Conflict | weakness | Incomplete | gap |  |
| CWE-437 | Incomplete Model of Endpoint Features | weakness | Incomplete | gap |  |
| CWE-438 | Behavioral Problems | category | Draft | taxonomy-only |  |
| CWE-439 | Behavioral Change in New Version or Environment | weakness | Draft | gap |  |
| CWE-440 | Expected Behavior Violation | weakness | Draft | gap |  |
| CWE-441 | Unintended Proxy or Intermediary ('Confused Deputy') | weakness | Draft | gap |  |
| CWE-442 | DEPRECATED: Web Problems | category | Deprecated | taxonomy-only |  |
| CWE-443 | DEPRECATED: HTTP response splitting | weakness | Deprecated | gap |  |
| CWE-444 | Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling') | weakness | Incomplete | gap |  |
| CWE-445 | DEPRECATED: User Interface Errors | category | Deprecated | taxonomy-only |  |
| CWE-446 | UI Discrepancy for Security Feature | weakness | Incomplete | gap |  |
| CWE-447 | Unimplemented or Unsupported Feature in UI | weakness | Draft | gap |  |
| CWE-448 | Obsolete Feature in UI | weakness | Draft | gap |  |
| CWE-449 | The UI Performs the Wrong Action | weakness | Incomplete | gap |  |
| CWE-450 | Multiple Interpretations of UI Input | weakness | Draft | gap |  |
| CWE-451 | User Interface (UI) Misrepresentation of Critical Information | weakness | Draft | gap |  |
| CWE-452 | Initialization and Cleanup Errors | category | Draft | taxonomy-only |  |
| CWE-453 | Insecure Default Variable Initialization | weakness | Draft | gap |  |
| CWE-454 | External Initialization of Trusted Variables or Data Stores | weakness | Draft | gap |  |
| CWE-455 | Non-exit on Failed Initialization | weakness | Draft | gap |  |
| CWE-456 | Missing Initialization of a Variable | weakness | Draft | gap |  |
| CWE-457 | Use of Uninitialized Variable | weakness | Draft | gap |  |
| CWE-458 | DEPRECATED: Incorrect Initialization | weakness | Deprecated | gap |  |
| CWE-459 | Incomplete Cleanup | weakness | Draft | gap |  |
| CWE-460 | Improper Cleanup on Thrown Exception | weakness | Draft | gap |  |
| CWE-461 | DEPRECATED: Data Structure Issues | category | Deprecated | taxonomy-only |  |
| CWE-462 | Duplicate Key in Associative List (Alist) | weakness | Incomplete | gap |  |
| CWE-463 | Deletion of Data Structure Sentinel | weakness | Incomplete | gap |  |
| CWE-464 | Addition of Data Structure Sentinel | weakness | Incomplete | gap |  |
| CWE-465 | Pointer Issues | category | Draft | taxonomy-only |  |
| CWE-466 | Return of Pointer Value Outside of Expected Range | weakness | Draft | gap |  |
| CWE-467 | Use of sizeof() on a Pointer Type | weakness | Draft | gap |  |
| CWE-468 | Incorrect Pointer Scaling | weakness | Incomplete | gap |  |
| CWE-469 | Use of Pointer Subtraction to Determine Size | weakness | Draft | gap |  |
| CWE-470 | Use of Externally-Controlled Input to Select Classes or Code ('Unsafe Reflection') | weakness | Draft | gap |  |
| CWE-471 | Modification of Assumed-Immutable Data (MAID) | weakness | Draft | gap |  |
| CWE-472 | External Control of Assumed-Immutable Web Parameter | weakness | Draft | gap |  |
| CWE-473 | PHP External Variable Modification | weakness | Draft | gap |  |
| CWE-474 | Use of Function with Inconsistent Implementations | weakness | Draft | gap |  |
| CWE-475 | Undefined Behavior for Input to API | weakness | Incomplete | gap |  |
| CWE-476 | NULL Pointer Dereference | weakness | Stable | implemented | [c/null-dereference](../labs/c/null-dereference/README.md), [cpp/null-dereference](../labs/cpp/null-dereference/README.md) |
| CWE-477 | Use of Obsolete Function | weakness | Draft | gap |  |
| CWE-478 | Missing Default Case in Multiple Condition Expression | weakness | Draft | gap |  |
| CWE-479 | Signal Handler Use of a Non-reentrant Function | weakness | Draft | gap |  |
| CWE-480 | Use of Incorrect Operator | weakness | Draft | gap |  |
| CWE-481 | Assigning instead of Comparing | weakness | Draft | gap |  |
| CWE-482 | Comparing instead of Assigning | weakness | Draft | gap |  |
| CWE-483 | Incorrect Block Delimitation | weakness | Draft | gap |  |
| CWE-484 | Omitted Break Statement in Switch | weakness | Draft | gap |  |
| CWE-485 | 7PK - Encapsulation | category | Draft | taxonomy-only |  |
| CWE-486 | Comparison of Classes by Name | weakness | Draft | gap |  |
| CWE-487 | Reliance on Package-level Scope | weakness | Incomplete | gap |  |
| CWE-488 | Exposure of Data Element to Wrong Session | weakness | Draft | gap |  |
| CWE-489 | Active Debug Code | weakness | Draft | implemented | [rest-api/legacy-endpoint](../labs/rest-api/legacy-endpoint/README.md) |
| CWE-490 | DEPRECATED: Mobile Code Issues | category | Deprecated | taxonomy-only |  |
| CWE-491 | Public cloneable() Method Without Final ('Object Hijack') | weakness | Draft | gap |  |
| CWE-492 | Use of Inner Class Containing Sensitive Data | weakness | Draft | gap |  |
| CWE-493 | Critical Public Variable Without Final Modifier | weakness | Draft | gap |  |
| CWE-494 | Download of Code Without Integrity Check | weakness | Draft | implemented | [python/unverified-update](../labs/python/unverified-update/README.md), [ai/model-artifact-integrity](../labs/ai/model-artifact-integrity/README.md) |
| CWE-495 | Private Data Structure Returned From A Public Method | weakness | Draft | gap |  |
| CWE-496 | Public Data Assigned to Private Array-Typed Field | weakness | Incomplete | gap |  |
| CWE-497 | Exposure of Sensitive System Information to an Unauthorized Control Sphere | weakness | Incomplete | gap |  |
| CWE-498 | Cloneable Class Containing Sensitive Information | weakness | Draft | gap |  |
| CWE-499 | Serializable Class Containing Sensitive Data | weakness | Draft | gap |  |
| CWE-500 | Public Static Field Not Marked Final | weakness | Draft | gap |  |
| CWE-501 | Trust Boundary Violation | weakness | Draft | gap |  |
| CWE-502 | Deserialization of Untrusted Data | weakness | Draft | implemented | [python/unsafe-deserialization](../labs/python/unsafe-deserialization/README.md) |
| CWE-503 | DEPRECATED: Byte/Object Code | category | Deprecated | taxonomy-only |  |
| CWE-504 | DEPRECATED: Motivation/Intent | category | Deprecated | taxonomy-only |  |
| CWE-505 | DEPRECATED: Intentionally Introduced Weakness | category | Deprecated | taxonomy-only |  |
| CWE-506 | Embedded Malicious Code | weakness | Incomplete | gap |  |
| CWE-507 | Trojan Horse | weakness | Incomplete | gap |  |
| CWE-508 | Non-Replicating Malicious Code | weakness | Incomplete | gap |  |
| CWE-509 | Replicating Malicious Code (Virus or Worm) | weakness | Incomplete | gap |  |
| CWE-510 | Trapdoor | weakness | Incomplete | gap |  |
| CWE-511 | Logic/Time Bomb | weakness | Incomplete | gap |  |
| CWE-512 | Spyware | weakness | Incomplete | gap |  |
| CWE-513 | DEPRECATED: Intentionally Introduced Nonmalicious Weakness | category | Deprecated | taxonomy-only |  |
| CWE-514 | Covert Channel | weakness | Incomplete | gap |  |
| CWE-515 | Covert Storage Channel | weakness | Incomplete | gap |  |
| CWE-516 | DEPRECATED: Covert Timing Channel | weakness | Deprecated | gap |  |
| CWE-517 | DEPRECATED: Other Intentional, Nonmalicious Weakness | category | Deprecated | taxonomy-only |  |
| CWE-518 | DEPRECATED: Inadvertently Introduced Weakness | category | Deprecated | taxonomy-only |  |
| CWE-519 | DEPRECATED: .NET Environment Issues | category | Deprecated | taxonomy-only |  |
| CWE-520 | .NET Misconfiguration: Use of Impersonation | weakness | Incomplete | gap |  |
| CWE-521 | Weak Password Requirements | weakness | Draft | gap |  |
| CWE-522 | Insufficiently Protected Credentials | weakness | Incomplete | gap |  |
| CWE-523 | Unprotected Transport of Credentials | weakness | Incomplete | gap |  |
| CWE-524 | Use of Cache Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-525 | Use of Web Browser Cache Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-526 | Cleartext Storage of Sensitive Information in an Environment Variable | weakness | Incomplete | gap |  |
| CWE-527 | Exposure of Version-Control Repository to an Unauthorized Control Sphere | weakness | Incomplete | gap |  |
| CWE-528 | Exposure of Core Dump File to an Unauthorized Control Sphere | weakness | Draft | gap |  |
| CWE-529 | Exposure of Access Control List Files to an Unauthorized Control Sphere | weakness | Incomplete | gap |  |
| CWE-530 | Exposure of Backup File to an Unauthorized Control Sphere | weakness | Incomplete | gap |  |
| CWE-531 | Inclusion of Sensitive Information in Test Code | weakness | Incomplete | gap |  |
| CWE-532 | Insertion of Sensitive Information into Log File | weakness | Incomplete | implemented | [python/sensitive-logging](../labs/python/sensitive-logging/README.md) |
| CWE-533 | DEPRECATED: Information Exposure Through Server Log Files | weakness | Deprecated | gap |  |
| CWE-534 | DEPRECATED: Information Exposure Through Debug Log Files | weakness | Deprecated | gap |  |
| CWE-535 | Exposure of Information Through Shell Error Message | weakness | Incomplete | gap |  |
| CWE-536 | Servlet Runtime Error Message Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-537 | Java Runtime Error Message Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-538 | Insertion of Sensitive Information into Externally-Accessible File or Directory | weakness | Draft | gap |  |
| CWE-539 | Use of Persistent Cookies Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-540 | Inclusion of Sensitive Information in Source Code | weakness | Incomplete | gap |  |
| CWE-541 | Inclusion of Sensitive Information in an Include File | weakness | Incomplete | gap |  |
| CWE-542 | DEPRECATED: Information Exposure Through Cleanup Log Files | weakness | Deprecated | gap |  |
| CWE-543 | Use of Singleton Pattern Without Synchronization in a Multithreaded Context | weakness | Incomplete | gap |  |
| CWE-544 | Missing Standardized Error Handling Mechanism | weakness | Draft | gap |  |
| CWE-545 | DEPRECATED: Use of Dynamic Class Loading | weakness | Deprecated | gap |  |
| CWE-546 | Suspicious Comment | weakness | Draft | gap |  |
| CWE-547 | Use of Hard-coded, Security-relevant Constants | weakness | Draft | gap |  |
| CWE-548 | Exposure of Information Through Directory Listing | weakness | Draft | gap |  |
| CWE-549 | Missing Password Field Masking | weakness | Draft | gap |  |
| CWE-550 | Server-generated Error Message Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-551 | Incorrect Behavior Order: Authorization Before Parsing and Canonicalization | weakness | Incomplete | gap |  |
| CWE-552 | Files or Directories Accessible to External Parties | weakness | Draft | gap |  |
| CWE-553 | Command Shell in Externally Accessible Directory | weakness | Incomplete | gap |  |
| CWE-554 | ASP.NET Misconfiguration: Not Using Input Validation Framework | weakness | Draft | gap |  |
| CWE-555 | J2EE Misconfiguration: Plaintext Password in Configuration File | weakness | Draft | gap |  |
| CWE-556 | ASP.NET Misconfiguration: Use of Identity Impersonation | weakness | Incomplete | gap |  |
| CWE-557 | Concurrency Issues | category | Draft | taxonomy-only |  |
| CWE-558 | Use of getlogin() in Multithreaded Application | weakness | Draft | gap |  |
| CWE-559 | DEPRECATED: Often Misused: Arguments and Parameters | category | Deprecated | taxonomy-only |  |
| CWE-560 | Use of umask() with chmod-style Argument | weakness | Draft | gap |  |
| CWE-561 | Dead Code | weakness | Draft | gap |  |
| CWE-562 | Return of Stack Variable Address | weakness | Draft | gap |  |
| CWE-563 | Assignment to Variable without Use | weakness | Draft | gap |  |
| CWE-564 | SQL Injection: Hibernate | weakness | Incomplete | gap |  |
| CWE-565 | Reliance on Cookies without Validation and Integrity Checking | weakness | Incomplete | gap |  |
| CWE-566 | Authorization Bypass Through User-Controlled SQL Primary Key | weakness | Incomplete | gap |  |
| CWE-567 | Unsynchronized Access to Shared Data in a Multithreaded Context | weakness | Draft | gap |  |
| CWE-568 | finalize() Method Without super.finalize() | weakness | Draft | gap |  |
| CWE-569 | Expression Issues | category | Draft | taxonomy-only |  |
| CWE-570 | Expression is Always False | weakness | Draft | gap |  |
| CWE-571 | Expression is Always True | weakness | Draft | gap |  |
| CWE-572 | Call to Thread run() instead of start() | weakness | Draft | gap |  |
| CWE-573 | Improper Following of Specification by Caller | weakness | Draft | gap |  |
| CWE-574 | EJB Bad Practices: Use of Synchronization Primitives | weakness | Draft | gap |  |
| CWE-575 | EJB Bad Practices: Use of AWT Swing | weakness | Draft | gap |  |
| CWE-576 | EJB Bad Practices: Use of Java I/O | weakness | Draft | gap |  |
| CWE-577 | EJB Bad Practices: Use of Sockets | weakness | Draft | gap |  |
| CWE-578 | EJB Bad Practices: Use of Class Loader | weakness | Draft | gap |  |
| CWE-579 | J2EE Bad Practices: Non-serializable Object Stored in Session | weakness | Draft | gap |  |
| CWE-580 | clone() Method Without super.clone() | weakness | Draft | gap |  |
| CWE-581 | Object Model Violation: Just One of Equals and Hashcode Defined | weakness | Draft | gap |  |
| CWE-582 | Array Declared Public, Final, and Static | weakness | Draft | gap |  |
| CWE-583 | finalize() Method Declared Public | weakness | Incomplete | gap |  |
| CWE-584 | Return Inside Finally Block | weakness | Draft | gap |  |
| CWE-585 | Empty Synchronized Block | weakness | Draft | gap |  |
| CWE-586 | Explicit Call to Finalize() | weakness | Draft | gap |  |
| CWE-587 | Assignment of a Fixed Address to a Pointer | weakness | Draft | gap |  |
| CWE-588 | Attempt to Access Child of a Non-structure Pointer | weakness | Incomplete | gap |  |
| CWE-589 | Call to Non-ubiquitous API | weakness | Incomplete | gap |  |
| CWE-590 | Free of Memory not on the Heap | weakness | Incomplete | gap |  |
| CWE-591 | Sensitive Data Storage in Improperly Locked Memory | weakness | Draft | gap |  |
| CWE-592 | DEPRECATED: Authentication Bypass Issues | weakness | Deprecated | gap |  |
| CWE-593 | Authentication Bypass: OpenSSL CTX Object Modified after SSL Objects are Created | weakness | Draft | gap |  |
| CWE-594 | J2EE Framework: Saving Unserializable Objects to Disk | weakness | Incomplete | gap |  |
| CWE-595 | Comparison of Object References Instead of Object Contents | weakness | Incomplete | gap |  |
| CWE-596 | DEPRECATED: Incorrect Semantic Object Comparison | weakness | Deprecated | gap |  |
| CWE-597 | Use of Wrong Operator in String Comparison | weakness | Draft | gap |  |
| CWE-598 | Use of HTTP Request With Sensitive Query String | weakness | Draft | gap |  |
| CWE-599 | Missing Validation of OpenSSL Certificate | weakness | Incomplete | gap |  |
| CWE-600 | Uncaught Exception in Servlet | weakness | Draft | gap |  |
| CWE-601 | URL Redirection to Untrusted Site ('Open Redirect') | weakness | Draft | implemented | [python/open-redirect](../labs/python/open-redirect/README.md), [cgi/open-redirect](../labs/cgi/open-redirect/README.md), [rest-api/open-redirect](../labs/rest-api/open-redirect/README.md), [ai/open-redirect](../labs/ai/open-redirect/README.md), [c/open-redirect](../labs/c/open-redirect/README.md), [cpp/open-redirect](../labs/cpp/open-redirect/README.md), [node/open-redirect](../labs/node/open-redirect/README.md), [typescript/open-redirect](../labs/typescript/open-redirect/README.md), [php/open-redirect](../labs/php/open-redirect/README.md), [ruby/open-redirect](../labs/ruby/open-redirect/README.md), [go/open-redirect](../labs/go/open-redirect/README.md), [java/open-redirect](../labs/java/open-redirect/README.md), [dotnet/open-redirect](../labs/dotnet/open-redirect/README.md), [rust/open-redirect](../labs/rust/open-redirect/README.md) |
| CWE-602 | Client-Side Enforcement of Server-Side Security | weakness | Draft | gap |  |
| CWE-603 | Use of Client-Side Authentication | weakness | Draft | gap |  |
| CWE-604 | Deprecated Entries | view | Draft | taxonomy-only |  |
| CWE-605 | Multiple Binds to the Same Port | weakness | Draft | gap |  |
| CWE-606 | Unchecked Input for Loop Condition | weakness | Draft | gap |  |
| CWE-607 | Public Static Final Field References Mutable Object | weakness | Draft | gap |  |
| CWE-608 | Struts: Non-private Field in ActionForm Class | weakness | Draft | gap |  |
| CWE-609 | Double-Checked Locking | weakness | Draft | gap |  |
| CWE-610 | Externally Controlled Reference to a Resource in Another Sphere | weakness | Draft | gap |  |
| CWE-611 | Improper Restriction of XML External Entity Reference | weakness | Draft | implemented | [java/xxe](../labs/java/xxe/README.md), [python/xxe](../labs/python/xxe/README.md) |
| CWE-612 | Improper Authorization of Index Containing Sensitive Information | weakness | Draft | gap |  |
| CWE-613 | Insufficient Session Expiration | weakness | Incomplete | gap |  |
| CWE-614 | Sensitive Cookie in HTTPS Session Without 'Secure' Attribute | weakness | Draft | gap |  |
| CWE-615 | Inclusion of Sensitive Information in Source Code Comments | weakness | Incomplete | gap |  |
| CWE-616 | Incomplete Identification of Uploaded File Variables (PHP) | weakness | Incomplete | gap |  |
| CWE-617 | Reachable Assertion | weakness | Draft | gap |  |
| CWE-618 | Exposed Unsafe ActiveX Method | weakness | Incomplete | gap |  |
| CWE-619 | Dangling Database Cursor ('Cursor Injection') | weakness | Incomplete | gap |  |
| CWE-620 | Unverified Password Change | weakness | Draft | gap |  |
| CWE-621 | Variable Extraction Error | weakness | Incomplete | gap |  |
| CWE-622 | Improper Validation of Function Hook Arguments | weakness | Draft | gap |  |
| CWE-623 | Unsafe ActiveX Control Marked Safe For Scripting | weakness | Draft | gap |  |
| CWE-624 | Executable Regular Expression Error | weakness | Incomplete | gap |  |
| CWE-625 | Permissive Regular Expression | weakness | Draft | gap |  |
| CWE-626 | Null Byte Interaction Error (Poison Null Byte) | weakness | Draft | gap |  |
| CWE-627 | Dynamic Variable Evaluation | weakness | Incomplete | gap |  |
| CWE-628 | Function Call with Incorrectly Specified Arguments | weakness | Draft | gap |  |
| CWE-629 | Weaknesses in OWASP Top Ten (2007) | view | Obsolete | taxonomy-only |  |
| CWE-630 | DEPRECATED: Weaknesses Examined by SAMATE | view | Deprecated | taxonomy-only |  |
| CWE-631 | DEPRECATED: Resource-specific Weaknesses | view | Deprecated | taxonomy-only |  |
| CWE-632 | DEPRECATED: Weaknesses that Affect Files or Directories | category | Deprecated | taxonomy-only |  |
| CWE-633 | DEPRECATED: Weaknesses that Affect Memory | category | Deprecated | taxonomy-only |  |
| CWE-634 | DEPRECATED: Weaknesses that Affect System Processes | category | Deprecated | taxonomy-only |  |
| CWE-635 | Weaknesses Originally Used by NVD from 2008 to 2016 | view | Obsolete | taxonomy-only |  |
| CWE-636 | Not Failing Securely ('Failing Open') | weakness | Draft | implemented | [python/fail-open](../labs/python/fail-open/README.md), [cgi/fail-open](../labs/cgi/fail-open/README.md), [rest-api/fail-open](../labs/rest-api/fail-open/README.md), [ai/fail-open](../labs/ai/fail-open/README.md), [c/fail-open](../labs/c/fail-open/README.md), [cpp/fail-open](../labs/cpp/fail-open/README.md), [node/fail-open](../labs/node/fail-open/README.md), [typescript/fail-open](../labs/typescript/fail-open/README.md), [php/fail-open](../labs/php/fail-open/README.md), [ruby/fail-open](../labs/ruby/fail-open/README.md), [go/fail-open](../labs/go/fail-open/README.md), [java/fail-open](../labs/java/fail-open/README.md), [dotnet/fail-open](../labs/dotnet/fail-open/README.md), [rust/fail-open](../labs/rust/fail-open/README.md) |
| CWE-637 | Unnecessary Complexity in Protection Mechanism (Not Using 'Economy of Mechanism') | weakness | Draft | gap |  |
| CWE-638 | Not Using Complete Mediation | weakness | Draft | gap |  |
| CWE-639 | Authorization Bypass Through User-Controlled Key | weakness | Incomplete | implemented | [python/idor](../labs/python/idor/README.md), [rest-api/bola](../labs/rest-api/bola/README.md), [cgi/idor](../labs/cgi/idor/README.md), [ai/idor](../labs/ai/idor/README.md), [c/idor](../labs/c/idor/README.md), [cpp/idor](../labs/cpp/idor/README.md), [node/idor](../labs/node/idor/README.md), [typescript/idor](../labs/typescript/idor/README.md), [php/idor](../labs/php/idor/README.md), [ruby/idor](../labs/ruby/idor/README.md), [go/idor](../labs/go/idor/README.md), [java/idor](../labs/java/idor/README.md), [dotnet/idor](../labs/dotnet/idor/README.md), [rust/idor](../labs/rust/idor/README.md) |
| CWE-640 | Weak Password Recovery Mechanism for Forgotten Password | weakness | Incomplete | gap |  |
| CWE-641 | Improper Restriction of Names for Files and Other Resources | weakness | Incomplete | gap |  |
| CWE-642 | External Control of Critical State Data | weakness | Draft | gap |  |
| CWE-643 | Improper Neutralization of Data within XPath Expressions ('XPath Injection') | weakness | Incomplete | gap |  |
| CWE-644 | Improper Neutralization of HTTP Headers for Scripting Syntax | weakness | Incomplete | gap |  |
| CWE-645 | Overly Restrictive Account Lockout Mechanism | weakness | Incomplete | gap |  |
| CWE-646 | Reliance on File Name or Extension of Externally-Supplied File | weakness | Incomplete | gap |  |
| CWE-647 | Use of Non-Canonical URL Paths for Authorization Decisions | weakness | Incomplete | gap |  |
| CWE-648 | Incorrect Use of Privileged APIs | weakness | Incomplete | gap |  |
| CWE-649 | Reliance on Obfuscation or Encryption of Security-Relevant Inputs without Integrity Checking | weakness | Incomplete | gap |  |
| CWE-650 | Trusting HTTP Permission Methods on the Server Side | weakness | Incomplete | gap |  |
| CWE-651 | Exposure of WSDL File Containing Sensitive Information | weakness | Incomplete | gap |  |
| CWE-652 | Improper Neutralization of Data within XQuery Expressions ('XQuery Injection') | weakness | Incomplete | gap |  |
| CWE-653 | Improper Isolation or Compartmentalization | weakness | Draft | gap |  |
| CWE-654 | Reliance on a Single Factor in a Security Decision | weakness | Draft | gap |  |
| CWE-655 | Insufficient Psychological Acceptability | weakness | Draft | gap |  |
| CWE-656 | Reliance on Security Through Obscurity | weakness | Draft | gap |  |
| CWE-657 | Violation of Secure Design Principles | weakness | Draft | gap |  |
| CWE-658 | Weaknesses in Software Written in C | view | Draft | taxonomy-only |  |
| CWE-659 | Weaknesses in Software Written in C++ | view | Draft | taxonomy-only |  |
| CWE-660 | Weaknesses in Software Written in Java | view | Draft | taxonomy-only |  |
| CWE-661 | Weaknesses in Software Written in PHP | view | Draft | taxonomy-only |  |
| CWE-662 | Improper Synchronization | weakness | Draft | gap |  |
| CWE-663 | Use of a Non-reentrant Function in a Concurrent Context | weakness | Draft | gap |  |
| CWE-664 | Improper Control of a Resource Through its Lifetime | weakness | Draft | gap |  |
| CWE-665 | Improper Initialization | weakness | Draft | gap |  |
| CWE-666 | Operation on Resource in Wrong Phase of Lifetime | weakness | Draft | gap |  |
| CWE-667 | Improper Locking | weakness | Draft | gap |  |
| CWE-668 | Exposure of Resource to Wrong Sphere | weakness | Draft | gap |  |
| CWE-669 | Incorrect Resource Transfer Between Spheres | weakness | Draft | gap |  |
| CWE-670 | Always-Incorrect Control Flow Implementation | weakness | Draft | gap |  |
| CWE-671 | Lack of Administrator Control over Security | weakness | Draft | gap |  |
| CWE-672 | Operation on a Resource after Expiration or Release | weakness | Draft | gap |  |
| CWE-673 | External Influence of Sphere Definition | weakness | Draft | gap |  |
| CWE-674 | Uncontrolled Recursion | weakness | Draft | gap |  |
| CWE-675 | Multiple Operations on Resource in Single-Operation Context | weakness | Draft | gap |  |
| CWE-676 | Use of Potentially Dangerous Function | weakness | Draft | gap |  |
| CWE-677 | Weakness Base Elements | view | Draft | taxonomy-only |  |
| CWE-678 | Composites | view | Draft | taxonomy-only |  |
| CWE-679 | DEPRECATED: Chain Elements | view | Deprecated | taxonomy-only |  |
| CWE-680 | Integer Overflow to Buffer Overflow | weakness | Draft | gap |  |
| CWE-681 | Incorrect Conversion between Numeric Types | weakness | Draft | gap |  |
| CWE-682 | Incorrect Calculation | weakness | Draft | gap |  |
| CWE-683 | Function Call With Incorrect Order of Arguments | weakness | Draft | gap |  |
| CWE-684 | Incorrect Provision of Specified Functionality | weakness | Draft | gap |  |
| CWE-685 | Function Call With Incorrect Number of Arguments | weakness | Draft | gap |  |
| CWE-686 | Function Call With Incorrect Argument Type | weakness | Draft | gap |  |
| CWE-687 | Function Call With Incorrectly Specified Argument Value | weakness | Draft | gap |  |
| CWE-688 | Function Call With Incorrect Variable or Reference as Argument | weakness | Draft | gap |  |
| CWE-689 | Permission Race Condition During Resource Copy | weakness | Draft | gap |  |
| CWE-690 | Unchecked Return Value to NULL Pointer Dereference | weakness | Draft | gap |  |
| CWE-691 | Insufficient Control Flow Management | weakness | Draft | gap |  |
| CWE-692 | Incomplete Denylist to Cross-Site Scripting | weakness | Draft | gap |  |
| CWE-693 | Protection Mechanism Failure | weakness | Draft | gap |  |
| CWE-694 | Use of Multiple Resources with Duplicate Identifier | weakness | Incomplete | gap |  |
| CWE-695 | Use of Low-Level Functionality | weakness | Incomplete | gap |  |
| CWE-696 | Incorrect Behavior Order | weakness | Incomplete | gap |  |
| CWE-697 | Incorrect Comparison | weakness | Incomplete | gap |  |
| CWE-698 | Execution After Redirect (EAR) | weakness | Incomplete | gap |  |
| CWE-699 | Software Development | view | Draft | taxonomy-only |  |
| CWE-700 | Seven Pernicious Kingdoms | view | Incomplete | taxonomy-only |  |
| CWE-701 | Weaknesses Introduced During Design | view | Incomplete | taxonomy-only |  |
| CWE-702 | Weaknesses Introduced During Implementation | view | Incomplete | taxonomy-only |  |
| CWE-703 | Improper Check or Handling of Exceptional Conditions | weakness | Incomplete | gap |  |
| CWE-704 | Incorrect Type Conversion or Cast | weakness | Incomplete | gap |  |
| CWE-705 | Incorrect Control Flow Scoping | weakness | Incomplete | gap |  |
| CWE-706 | Use of Incorrectly-Resolved Name or Reference | weakness | Incomplete | gap |  |
| CWE-707 | Improper Neutralization | weakness | Incomplete | gap |  |
| CWE-708 | Incorrect Ownership Assignment | weakness | Incomplete | gap |  |
| CWE-709 | Named Chains | view | Incomplete | taxonomy-only |  |
| CWE-710 | Improper Adherence to Coding Standards | weakness | Incomplete | gap |  |
| CWE-711 | Weaknesses in OWASP Top Ten (2004) | view | Obsolete | taxonomy-only |  |
| CWE-712 | OWASP Top Ten 2007 Category A1 - Cross Site Scripting (XSS) | category | Obsolete | taxonomy-only |  |
| CWE-713 | OWASP Top Ten 2007 Category A2 - Injection Flaws | category | Obsolete | taxonomy-only |  |
| CWE-714 | OWASP Top Ten 2007 Category A3 - Malicious File Execution | category | Obsolete | taxonomy-only |  |
| CWE-715 | OWASP Top Ten 2007 Category A4 - Insecure Direct Object Reference | category | Obsolete | taxonomy-only |  |
| CWE-716 | OWASP Top Ten 2007 Category A5 - Cross Site Request Forgery (CSRF) | category | Obsolete | taxonomy-only |  |
| CWE-717 | OWASP Top Ten 2007 Category A6 - Information Leakage and Improper Error Handling | category | Obsolete | taxonomy-only |  |
| CWE-718 | OWASP Top Ten 2007 Category A7 - Broken Authentication and Session Management | category | Obsolete | taxonomy-only |  |
| CWE-719 | OWASP Top Ten 2007 Category A8 - Insecure Cryptographic Storage | category | Obsolete | taxonomy-only |  |
| CWE-720 | OWASP Top Ten 2007 Category A9 - Insecure Communications | category | Obsolete | taxonomy-only |  |
| CWE-721 | OWASP Top Ten 2007 Category A10 - Failure to Restrict URL Access | category | Obsolete | taxonomy-only |  |
| CWE-722 | OWASP Top Ten 2004 Category A1 - Unvalidated Input | category | Obsolete | taxonomy-only |  |
| CWE-723 | OWASP Top Ten 2004 Category A2 - Broken Access Control | category | Obsolete | taxonomy-only |  |
| CWE-724 | OWASP Top Ten 2004 Category A3 - Broken Authentication and Session Management | category | Obsolete | taxonomy-only |  |
| CWE-725 | OWASP Top Ten 2004 Category A4 - Cross-Site Scripting (XSS) Flaws | category | Obsolete | taxonomy-only |  |
| CWE-726 | OWASP Top Ten 2004 Category A5 - Buffer Overflows | category | Obsolete | taxonomy-only |  |
| CWE-727 | OWASP Top Ten 2004 Category A6 - Injection Flaws | category | Obsolete | taxonomy-only |  |
| CWE-728 | OWASP Top Ten 2004 Category A7 - Improper Error Handling | category | Obsolete | taxonomy-only |  |
| CWE-729 | OWASP Top Ten 2004 Category A8 - Insecure Storage | category | Obsolete | taxonomy-only |  |
| CWE-730 | OWASP Top Ten 2004 Category A9 - Denial of Service | category | Obsolete | taxonomy-only |  |
| CWE-731 | OWASP Top Ten 2004 Category A10 - Insecure Configuration Management | category | Obsolete | taxonomy-only |  |
| CWE-732 | Incorrect Permission Assignment for Critical Resource | weakness | Draft | implemented | [python/world-readable-secret](../labs/python/world-readable-secret/README.md), [cgi/world-readable-secret](../labs/cgi/world-readable-secret/README.md), [rest-api/world-readable-secret](../labs/rest-api/world-readable-secret/README.md), [ai/world-readable-secret](../labs/ai/world-readable-secret/README.md), [c/world-readable-secret](../labs/c/world-readable-secret/README.md), [cpp/world-readable-secret](../labs/cpp/world-readable-secret/README.md), [node/world-readable-secret](../labs/node/world-readable-secret/README.md), [typescript/world-readable-secret](../labs/typescript/world-readable-secret/README.md), [php/world-readable-secret](../labs/php/world-readable-secret/README.md), [ruby/world-readable-secret](../labs/ruby/world-readable-secret/README.md), [go/world-readable-secret](../labs/go/world-readable-secret/README.md), [java/world-readable-secret](../labs/java/world-readable-secret/README.md), [dotnet/world-readable-secret](../labs/dotnet/world-readable-secret/README.md), [rust/world-readable-secret](../labs/rust/world-readable-secret/README.md) |
| CWE-733 | Compiler Optimization Removal or Modification of Security-critical Code | weakness | Incomplete | gap |  |
| CWE-734 | Weaknesses Addressed by the CERT C Secure Coding Standard (2008) | view | Obsolete | taxonomy-only |  |
| CWE-735 | CERT C Secure Coding Standard (2008) Chapter 2 - Preprocessor (PRE) | category | Obsolete | taxonomy-only |  |
| CWE-736 | CERT C Secure Coding Standard (2008) Chapter 3 - Declarations and Initialization (DCL) | category | Obsolete | taxonomy-only |  |
| CWE-737 | CERT C Secure Coding Standard (2008) Chapter 4 - Expressions (EXP) | category | Obsolete | taxonomy-only |  |
| CWE-738 | CERT C Secure Coding Standard (2008) Chapter 5 - Integers (INT) | category | Obsolete | taxonomy-only |  |
| CWE-739 | CERT C Secure Coding Standard (2008) Chapter 6 - Floating Point (FLP) | category | Obsolete | taxonomy-only |  |
| CWE-740 | CERT C Secure Coding Standard (2008) Chapter 7 - Arrays (ARR) | category | Obsolete | taxonomy-only |  |
| CWE-741 | CERT C Secure Coding Standard (2008) Chapter 8 - Characters and Strings (STR) | category | Obsolete | taxonomy-only |  |
| CWE-742 | CERT C Secure Coding Standard (2008) Chapter 9 - Memory Management (MEM) | category | Obsolete | taxonomy-only |  |
| CWE-743 | CERT C Secure Coding Standard (2008) Chapter 10 - Input Output (FIO) | category | Obsolete | taxonomy-only |  |
| CWE-744 | CERT C Secure Coding Standard (2008) Chapter 11 - Environment (ENV) | category | Obsolete | taxonomy-only |  |
| CWE-745 | CERT C Secure Coding Standard (2008) Chapter 12 - Signals (SIG) | category | Obsolete | taxonomy-only |  |
| CWE-746 | CERT C Secure Coding Standard (2008) Chapter 13 - Error Handling (ERR) | category | Obsolete | taxonomy-only |  |
| CWE-747 | CERT C Secure Coding Standard (2008) Chapter 14 - Miscellaneous (MSC) | category | Obsolete | taxonomy-only |  |
| CWE-748 | CERT C Secure Coding Standard (2008) Appendix - POSIX (POS) | category | Obsolete | taxonomy-only |  |
| CWE-749 | Exposed Dangerous Method or Function | weakness | Incomplete | gap |  |
| CWE-750 | Weaknesses in the 2009 CWE/SANS Top 25 Most Dangerous Programming Errors | view | Obsolete | taxonomy-only |  |
| CWE-751 | 2009 Top 25 - Insecure Interaction Between Components | category | Obsolete | taxonomy-only |  |
| CWE-752 | 2009 Top 25 - Risky Resource Management | category | Obsolete | taxonomy-only |  |
| CWE-753 | 2009 Top 25 - Porous Defenses | category | Obsolete | taxonomy-only |  |
| CWE-754 | Improper Check for Unusual or Exceptional Conditions | weakness | Incomplete | gap |  |
| CWE-755 | Improper Handling of Exceptional Conditions | weakness | Incomplete | gap |  |
| CWE-756 | Missing Custom Error Page | weakness | Incomplete | gap |  |
| CWE-757 | Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade') | weakness | Incomplete | gap |  |
| CWE-758 | Reliance on Undefined, Unspecified, or Implementation-Defined Behavior | weakness | Incomplete | gap |  |
| CWE-759 | Use of a One-Way Hash without a Salt | weakness | Incomplete | gap |  |
| CWE-760 | Use of a One-Way Hash with a Predictable Salt | weakness | Incomplete | gap |  |
| CWE-761 | Free of Pointer not at Start of Buffer | weakness | Incomplete | gap |  |
| CWE-762 | Mismatched Memory Management Routines | weakness | Incomplete | gap |  |
| CWE-763 | Release of Invalid Pointer or Reference | weakness | Incomplete | gap |  |
| CWE-764 | Multiple Locks of a Critical Resource | weakness | Incomplete | gap |  |
| CWE-765 | Multiple Unlocks of a Critical Resource | weakness | Incomplete | gap |  |
| CWE-766 | Critical Data Element Declared Public | weakness | Incomplete | gap |  |
| CWE-767 | Access to Critical Private Variable via Public Method | weakness | Incomplete | gap |  |
| CWE-768 | Incorrect Short Circuit Evaluation | weakness | Incomplete | gap |  |
| CWE-769 | DEPRECATED: Uncontrolled File Descriptor Consumption | weakness | Deprecated | gap |  |
| CWE-770 | Allocation of Resources Without Limits or Throttling | weakness | Incomplete | implemented | [rest-api/resource-consumption](../labs/rest-api/resource-consumption/README.md) |
| CWE-771 | Missing Reference to Active Allocated Resource | weakness | Incomplete | gap |  |
| CWE-772 | Missing Release of Resource after Effective Lifetime | weakness | Draft | gap |  |
| CWE-773 | Missing Reference to Active File Descriptor or Handle | weakness | Incomplete | gap |  |
| CWE-774 | Allocation of File Descriptors or Handles Without Limits or Throttling | weakness | Incomplete | gap |  |
| CWE-775 | Missing Release of File Descriptor or Handle after Effective Lifetime | weakness | Incomplete | gap |  |
| CWE-776 | Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion') | weakness | Draft | gap |  |
| CWE-777 | Regular Expression without Anchors | weakness | Incomplete | gap |  |
| CWE-778 | Insufficient Logging | weakness | Draft | implemented | [python/missing-audit](../labs/python/missing-audit/README.md) |
| CWE-779 | Logging of Excessive Data | weakness | Draft | gap |  |
| CWE-780 | Use of RSA Algorithm without OAEP | weakness | Incomplete | gap |  |
| CWE-781 | Improper Address Validation in IOCTL with METHOD_NEITHER I/O Control Code | weakness | Draft | gap |  |
| CWE-782 | Exposed IOCTL with Insufficient Access Control | weakness | Draft | gap |  |
| CWE-783 | Operator Precedence Logic Error | weakness | Draft | gap |  |
| CWE-784 | Reliance on Cookies without Validation and Integrity Checking in a Security Decision | weakness | Draft | gap |  |
| CWE-785 | Use of Path Manipulation Function without Maximum-sized Buffer | weakness | Incomplete | gap |  |
| CWE-786 | Access of Memory Location Before Start of Buffer | weakness | Incomplete | gap |  |
| CWE-787 | Out-of-bounds Write | weakness | Draft | gap |  |
| CWE-788 | Access of Memory Location After End of Buffer | weakness | Incomplete | gap |  |
| CWE-789 | Memory Allocation with Excessive Size Value | weakness | Draft | gap |  |
| CWE-790 | Improper Filtering of Special Elements | weakness | Incomplete | gap |  |
| CWE-791 | Incomplete Filtering of Special Elements | weakness | Incomplete | gap |  |
| CWE-792 | Incomplete Filtering of One or More Instances of Special Elements | weakness | Incomplete | gap |  |
| CWE-793 | Only Filtering One Instance of a Special Element | weakness | Incomplete | gap |  |
| CWE-794 | Incomplete Filtering of Multiple Instances of Special Elements | weakness | Incomplete | gap |  |
| CWE-795 | Only Filtering Special Elements at a Specified Location | weakness | Incomplete | gap |  |
| CWE-796 | Only Filtering Special Elements Relative to a Marker | weakness | Incomplete | gap |  |
| CWE-797 | Only Filtering Special Elements at an Absolute Position | weakness | Incomplete | gap |  |
| CWE-798 | Use of Hard-coded Credentials | weakness | Draft | implemented | [python/hardcoded-credentials](../labs/python/hardcoded-credentials/README.md), [cgi/hardcoded-credentials](../labs/cgi/hardcoded-credentials/README.md), [rest-api/hardcoded-credentials](../labs/rest-api/hardcoded-credentials/README.md), [ai/hardcoded-credentials](../labs/ai/hardcoded-credentials/README.md), [c/hardcoded-credentials](../labs/c/hardcoded-credentials/README.md), [cpp/hardcoded-credentials](../labs/cpp/hardcoded-credentials/README.md), [node/hardcoded-credentials](../labs/node/hardcoded-credentials/README.md), [typescript/hardcoded-credentials](../labs/typescript/hardcoded-credentials/README.md), [php/hardcoded-credentials](../labs/php/hardcoded-credentials/README.md), [ruby/hardcoded-credentials](../labs/ruby/hardcoded-credentials/README.md), [go/hardcoded-credentials](../labs/go/hardcoded-credentials/README.md), [java/hardcoded-credentials](../labs/java/hardcoded-credentials/README.md), [dotnet/hardcoded-credentials](../labs/dotnet/hardcoded-credentials/README.md), [rust/hardcoded-credentials](../labs/rust/hardcoded-credentials/README.md) |
| CWE-799 | Improper Control of Interaction Frequency | weakness | Incomplete | implemented | [rest-api/business-flow-abuse](../labs/rest-api/business-flow-abuse/README.md) |
| CWE-800 | Weaknesses in the 2010 CWE/SANS Top 25 Most Dangerous Programming Errors | view | Obsolete | taxonomy-only |  |
| CWE-801 | 2010 Top 25 - Insecure Interaction Between Components | category | Obsolete | taxonomy-only |  |
| CWE-802 | 2010 Top 25 - Risky Resource Management | category | Obsolete | taxonomy-only |  |
| CWE-803 | 2010 Top 25 - Porous Defenses | category | Obsolete | taxonomy-only |  |
| CWE-804 | Guessable CAPTCHA | weakness | Incomplete | gap |  |
| CWE-805 | Buffer Access with Incorrect Length Value | weakness | Incomplete | gap |  |
| CWE-806 | Buffer Access Using Size of Source Buffer | weakness | Incomplete | gap |  |
| CWE-807 | Reliance on Untrusted Inputs in a Security Decision | weakness | Incomplete | gap |  |
| CWE-808 | 2010 Top 25 - Weaknesses On the Cusp | category | Obsolete | taxonomy-only |  |
| CWE-809 | Weaknesses in OWASP Top Ten (2010) | view | Obsolete | taxonomy-only |  |
| CWE-810 | OWASP Top Ten 2010 Category A1 - Injection | category | Obsolete | taxonomy-only |  |
| CWE-811 | OWASP Top Ten 2010 Category A2 - Cross-Site Scripting (XSS) | category | Obsolete | taxonomy-only |  |
| CWE-812 | OWASP Top Ten 2010 Category A3 - Broken Authentication and Session Management | category | Obsolete | taxonomy-only |  |
| CWE-813 | OWASP Top Ten 2010 Category A4 - Insecure Direct Object References | category | Obsolete | taxonomy-only |  |
| CWE-814 | OWASP Top Ten 2010 Category A5 - Cross-Site Request Forgery(CSRF) | category | Obsolete | taxonomy-only |  |
| CWE-815 | OWASP Top Ten 2010 Category A6 - Security Misconfiguration | category | Obsolete | taxonomy-only |  |
| CWE-816 | OWASP Top Ten 2010 Category A7 - Insecure Cryptographic Storage | category | Obsolete | taxonomy-only |  |
| CWE-817 | OWASP Top Ten 2010 Category A8 - Failure to Restrict URL Access | category | Obsolete | taxonomy-only |  |
| CWE-818 | OWASP Top Ten 2010 Category A9 - Insufficient Transport Layer Protection | category | Obsolete | taxonomy-only |  |
| CWE-819 | OWASP Top Ten 2010 Category A10 - Unvalidated Redirects and Forwards | category | Obsolete | taxonomy-only |  |
| CWE-820 | Missing Synchronization | weakness | Incomplete | gap |  |
| CWE-821 | Incorrect Synchronization | weakness | Incomplete | gap |  |
| CWE-822 | Untrusted Pointer Dereference | weakness | Incomplete | gap |  |
| CWE-823 | Use of Out-of-range Pointer Offset | weakness | Incomplete | gap |  |
| CWE-824 | Access of Uninitialized Pointer | weakness | Incomplete | gap |  |
| CWE-825 | Expired Pointer Dereference | weakness | Incomplete | gap |  |
| CWE-826 | Premature Release of Resource During Expected Lifetime | weakness | Incomplete | gap |  |
| CWE-827 | Improper Control of Document Type Definition | weakness | Incomplete | gap |  |
| CWE-828 | Signal Handler with Functionality that is not Asynchronous-Safe | weakness | Incomplete | gap |  |
| CWE-829 | Inclusion of Functionality from Untrusted Control Sphere | weakness | Incomplete | implemented | [python/untrusted-plugin](../labs/python/untrusted-plugin/README.md) |
| CWE-830 | Inclusion of Web Functionality from an Untrusted Source | weakness | Incomplete | gap |  |
| CWE-831 | Signal Handler Function Associated with Multiple Signals | weakness | Incomplete | gap |  |
| CWE-832 | Unlock of a Resource that is not Locked | weakness | Incomplete | gap |  |
| CWE-833 | Deadlock | weakness | Incomplete | gap |  |
| CWE-834 | Excessive Iteration | weakness | Incomplete | implemented | [ai/unbounded-agent-loop](../labs/ai/unbounded-agent-loop/README.md) |
| CWE-835 | Loop with Unreachable Exit Condition ('Infinite Loop') | weakness | Incomplete | gap |  |
| CWE-836 | Use of Password Hash Instead of Password for Authentication | weakness | Incomplete | gap |  |
| CWE-837 | Improper Enforcement of a Single, Unique Action | weakness | Incomplete | gap |  |
| CWE-838 | Inappropriate Encoding for Output Context | weakness | Incomplete | gap |  |
| CWE-839 | Numeric Range Comparison Without Minimum Check | weakness | Incomplete | gap |  |
| CWE-840 | Business Logic Errors | category | Incomplete | taxonomy-only |  |
| CWE-841 | Improper Enforcement of Behavioral Workflow | weakness | Incomplete | implemented | [rest-api/order-workflow](../labs/rest-api/order-workflow/README.md) |
| CWE-842 | Placement of User into Incorrect Group | weakness | Incomplete | gap |  |
| CWE-843 | Access of Resource Using Incompatible Type ('Type Confusion') | weakness | Incomplete | gap |  |
| CWE-844 | Weaknesses Addressed by The CERT Oracle Secure Coding Standard for Java (2011) | view | Obsolete | taxonomy-only |  |
| CWE-845 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 2 - Input Validation and Data Sanitization (IDS) | category | Obsolete | taxonomy-only |  |
| CWE-846 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 3 - Declarations and Initialization (DCL) | category | Obsolete | taxonomy-only |  |
| CWE-847 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 4 - Expressions (EXP) | category | Obsolete | taxonomy-only |  |
| CWE-848 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 5 - Numeric Types and Operations (NUM) | category | Obsolete | taxonomy-only |  |
| CWE-849 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 6 - Object Orientation (OBJ) | category | Obsolete | taxonomy-only |  |
| CWE-850 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 7 - Methods (MET) | category | Obsolete | taxonomy-only |  |
| CWE-851 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 8 - Exceptional Behavior (ERR) | category | Obsolete | taxonomy-only |  |
| CWE-852 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 9 - Visibility and Atomicity (VNA) | category | Obsolete | taxonomy-only |  |
| CWE-853 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 10 - Locking (LCK) | category | Obsolete | taxonomy-only |  |
| CWE-854 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 11 - Thread APIs (THI) | category | Obsolete | taxonomy-only |  |
| CWE-855 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 12 - Thread Pools (TPS) | category | Obsolete | taxonomy-only |  |
| CWE-856 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 13 - Thread-Safety Miscellaneous (TSM) | category | Obsolete | taxonomy-only |  |
| CWE-857 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 14 - Input Output (FIO) | category | Obsolete | taxonomy-only |  |
| CWE-858 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 15 - Serialization (SER) | category | Obsolete | taxonomy-only |  |
| CWE-859 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 16 - Platform Security (SEC) | category | Obsolete | taxonomy-only |  |
| CWE-860 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 17 - Runtime Environment (ENV) | category | Obsolete | taxonomy-only |  |
| CWE-861 | The CERT Oracle Secure Coding Standard for Java (2011) Chapter 18 - Miscellaneous (MSC) | category | Obsolete | taxonomy-only |  |
| CWE-862 | Missing Authorization | weakness | Incomplete | implemented | [rest-api/function-authorization](../labs/rest-api/function-authorization/README.md), [ai/excessive-agency](../labs/ai/excessive-agency/README.md), [python/missing-authorization](../labs/python/missing-authorization/README.md), [cgi/missing-authorization](../labs/cgi/missing-authorization/README.md), [c/missing-authorization](../labs/c/missing-authorization/README.md), [cpp/missing-authorization](../labs/cpp/missing-authorization/README.md), [node/missing-authorization](../labs/node/missing-authorization/README.md), [typescript/missing-authorization](../labs/typescript/missing-authorization/README.md), [php/missing-authorization](../labs/php/missing-authorization/README.md), [ruby/missing-authorization](../labs/ruby/missing-authorization/README.md), [go/missing-authorization](../labs/go/missing-authorization/README.md), [java/missing-authorization](../labs/java/missing-authorization/README.md), [dotnet/missing-authorization](../labs/dotnet/missing-authorization/README.md), [rust/missing-authorization](../labs/rust/missing-authorization/README.md) |
| CWE-863 | Incorrect Authorization | weakness | Incomplete | implemented | [ai/cross-tenant-retrieval](../labs/ai/cross-tenant-retrieval/README.md), [rest-api/multi-tenant-authorization](../labs/rest-api/multi-tenant-authorization/README.md), [ai/tool-argument-scope](../labs/ai/tool-argument-scope/README.md), [python/jwt-disabled-user](../labs/python/jwt-disabled-user/README.md) |
| CWE-864 | 2011 Top 25 - Insecure Interaction Between Components | category | Obsolete | taxonomy-only |  |
| CWE-865 | 2011 Top 25 - Risky Resource Management | category | Obsolete | taxonomy-only |  |
| CWE-866 | 2011 Top 25 - Porous Defenses | category | Obsolete | taxonomy-only |  |
| CWE-867 | 2011 Top 25 - Weaknesses On the Cusp | category | Obsolete | taxonomy-only |  |
| CWE-868 | Weaknesses Addressed by the SEI CERT C++ Coding Standard (2016 Version) | view | Obsolete | taxonomy-only |  |
| CWE-869 | CERT C++ Secure Coding Section 01 - Preprocessor (PRE) | category | Incomplete | taxonomy-only |  |
| CWE-870 | CERT C++ Secure Coding Section 02 - Declarations and Initialization (DCL) | category | Incomplete | taxonomy-only |  |
| CWE-871 | CERT C++ Secure Coding Section 03 - Expressions (EXP) | category | Incomplete | taxonomy-only |  |
| CWE-872 | CERT C++ Secure Coding Section 04 - Integers (INT) | category | Incomplete | taxonomy-only |  |
| CWE-873 | CERT C++ Secure Coding Section 05 - Floating Point Arithmetic (FLP) | category | Incomplete | taxonomy-only |  |
| CWE-874 | CERT C++ Secure Coding Section 06 - Arrays and the STL (ARR) | category | Incomplete | taxonomy-only |  |
| CWE-875 | CERT C++ Secure Coding Section 07 - Characters and Strings (STR) | category | Incomplete | taxonomy-only |  |
| CWE-876 | CERT C++ Secure Coding Section 08 - Memory Management (MEM) | category | Incomplete | taxonomy-only |  |
| CWE-877 | CERT C++ Secure Coding Section 09 - Input Output (FIO) | category | Incomplete | taxonomy-only |  |
| CWE-878 | CERT C++ Secure Coding Section 10 - Environment (ENV) | category | Incomplete | taxonomy-only |  |
| CWE-879 | CERT C++ Secure Coding Section 11 - Signals (SIG) | category | Incomplete | taxonomy-only |  |
| CWE-880 | CERT C++ Secure Coding Section 12 - Exceptions and Error Handling (ERR) | category | Incomplete | taxonomy-only |  |
| CWE-881 | CERT C++ Secure Coding Section 13 - Object Oriented Programming (OOP) | category | Incomplete | taxonomy-only |  |
| CWE-882 | CERT C++ Secure Coding Section 14 - Concurrency (CON) | category | Incomplete | taxonomy-only |  |
| CWE-883 | CERT C++ Secure Coding Section 49 - Miscellaneous (MSC) | category | Incomplete | taxonomy-only |  |
| CWE-884 | CWE Cross-section | view | Incomplete | taxonomy-only |  |
| CWE-885 | SFP Primary Cluster: Risky Values | category | Incomplete | taxonomy-only |  |
| CWE-886 | SFP Primary Cluster: Unused entities | category | Incomplete | taxonomy-only |  |
| CWE-887 | SFP Primary Cluster: API | category | Incomplete | taxonomy-only |  |
| CWE-888 | Software Fault Pattern (SFP) Clusters | view | Incomplete | taxonomy-only |  |
| CWE-889 | SFP Primary Cluster: Exception Management | category | Incomplete | taxonomy-only |  |
| CWE-890 | SFP Primary Cluster: Memory Access | category | Incomplete | taxonomy-only |  |
| CWE-891 | SFP Primary Cluster: Memory Management | category | Incomplete | taxonomy-only |  |
| CWE-892 | SFP Primary Cluster: Resource Management | category | Incomplete | taxonomy-only |  |
| CWE-893 | SFP Primary Cluster: Path Resolution | category | Incomplete | taxonomy-only |  |
| CWE-894 | SFP Primary Cluster: Synchronization | category | Incomplete | taxonomy-only |  |
| CWE-895 | SFP Primary Cluster: Information Leak | category | Incomplete | taxonomy-only |  |
| CWE-896 | SFP Primary Cluster: Tainted Input | category | Incomplete | taxonomy-only |  |
| CWE-897 | SFP Primary Cluster: Entry Points | category | Incomplete | taxonomy-only |  |
| CWE-898 | SFP Primary Cluster: Authentication | category | Incomplete | taxonomy-only |  |
| CWE-899 | SFP Primary Cluster: Access Control | category | Incomplete | taxonomy-only |  |
| CWE-900 | Weaknesses in the 2011 CWE/SANS Top 25 Most Dangerous Software Errors | view | Obsolete | taxonomy-only |  |
| CWE-901 | SFP Primary Cluster: Privilege | category | Incomplete | taxonomy-only |  |
| CWE-902 | SFP Primary Cluster: Channel | category | Incomplete | taxonomy-only |  |
| CWE-903 | SFP Primary Cluster: Cryptography | category | Incomplete | taxonomy-only |  |
| CWE-904 | SFP Primary Cluster: Malware | category | Incomplete | taxonomy-only |  |
| CWE-905 | SFP Primary Cluster: Predictability | category | Incomplete | taxonomy-only |  |
| CWE-906 | SFP Primary Cluster: UI | category | Incomplete | taxonomy-only |  |
| CWE-907 | SFP Primary Cluster: Other | category | Incomplete | taxonomy-only |  |
| CWE-908 | Use of Uninitialized Resource | weakness | Incomplete | gap |  |
| CWE-909 | Missing Initialization of Resource | weakness | Incomplete | gap |  |
| CWE-910 | Use of Expired File Descriptor | weakness | Incomplete | gap |  |
| CWE-911 | Improper Update of Reference Count | weakness | Incomplete | gap |  |
| CWE-912 | Hidden Functionality | weakness | Incomplete | gap |  |
| CWE-913 | Improper Control of Dynamically-Managed Code Resources | weakness | Incomplete | gap |  |
| CWE-914 | Improper Control of Dynamically-Identified Variables | weakness | Incomplete | gap |  |
| CWE-915 | Improperly Controlled Modification of Dynamically-Determined Object Attributes | weakness | Incomplete | implemented | [python/mass-assignment](../labs/python/mass-assignment/README.md), [rest-api/property-authorization](../labs/rest-api/property-authorization/README.md) |
| CWE-916 | Use of Password Hash With Insufficient Computational Effort | weakness | Incomplete | implemented | [python/weak-password-hash](../labs/python/weak-password-hash/README.md) |
| CWE-917 | Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection') | weakness | Incomplete | gap |  |
| CWE-918 | Server-Side Request Forgery (SSRF) | weakness | Incomplete | implemented | [rest-api/ssrf](../labs/rest-api/ssrf/README.md), [rest-api/ssrf-redirect](../labs/rest-api/ssrf-redirect/README.md) |
| CWE-919 | Weaknesses in Mobile Applications | view | Incomplete | taxonomy-only |  |
| CWE-920 | Improper Restriction of Power Consumption | weakness | Incomplete | gap |  |
| CWE-921 | Storage of Sensitive Data in a Mechanism without Access Control | weakness | Incomplete | gap |  |
| CWE-922 | Insecure Storage of Sensitive Information | weakness | Incomplete | gap |  |
| CWE-923 | Improper Restriction of Communication Channel to Intended Endpoints | weakness | Incomplete | gap |  |
| CWE-924 | Improper Enforcement of Message Integrity During Transmission in a Communication Channel | weakness | Incomplete | gap |  |
| CWE-925 | Improper Verification of Intent by Broadcast Receiver | weakness | Incomplete | gap |  |
| CWE-926 | Improper Export of Android Application Components | weakness | Incomplete | gap |  |
| CWE-927 | Use of Implicit Intent for Sensitive Communication | weakness | Incomplete | gap |  |
| CWE-928 | Weaknesses in OWASP Top Ten (2013) | view | Obsolete | taxonomy-only |  |
| CWE-929 | OWASP Top Ten 2013 Category A1 - Injection | category | Obsolete | taxonomy-only |  |
| CWE-930 | OWASP Top Ten 2013 Category A2 - Broken Authentication and Session Management | category | Obsolete | taxonomy-only |  |
| CWE-931 | OWASP Top Ten 2013 Category A3 - Cross-Site Scripting (XSS) | category | Obsolete | taxonomy-only |  |
| CWE-932 | OWASP Top Ten 2013 Category A4 - Insecure Direct Object References | category | Obsolete | taxonomy-only |  |
| CWE-933 | OWASP Top Ten 2013 Category A5 - Security Misconfiguration | category | Obsolete | taxonomy-only |  |
| CWE-934 | OWASP Top Ten 2013 Category A6 - Sensitive Data Exposure | category | Obsolete | taxonomy-only |  |
| CWE-935 | OWASP Top Ten 2013 Category A7 - Missing Function Level Access Control | category | Obsolete | taxonomy-only |  |
| CWE-936 | OWASP Top Ten 2013 Category A8 - Cross-Site Request Forgery (CSRF) | category | Obsolete | taxonomy-only |  |
| CWE-937 | OWASP Top Ten 2013 Category A9 - Using Components with Known Vulnerabilities | category | Obsolete | taxonomy-only |  |
| CWE-938 | OWASP Top Ten 2013 Category A10 - Unvalidated Redirects and Forwards | category | Obsolete | taxonomy-only |  |
| CWE-939 | Improper Authorization in Handler for Custom URL Scheme | weakness | Incomplete | gap |  |
| CWE-940 | Improper Verification of Source of a Communication Channel | weakness | Incomplete | gap |  |
| CWE-941 | Incorrectly Specified Destination in a Communication Channel | weakness | Incomplete | gap |  |
| CWE-942 | Permissive Cross-domain Security Policy with Untrusted Domains | weakness | Incomplete | implemented | [rest-api/cors-misconfiguration](../labs/rest-api/cors-misconfiguration/README.md) |
| CWE-943 | Improper Neutralization of Special Elements in Data Query Logic | weakness | Incomplete | gap |  |
| CWE-944 | SFP Secondary Cluster: Access Management | category | Incomplete | taxonomy-only |  |
| CWE-945 | SFP Secondary Cluster: Insecure Resource Access | category | Incomplete | taxonomy-only |  |
| CWE-946 | SFP Secondary Cluster: Insecure Resource Permissions | category | Incomplete | taxonomy-only |  |
| CWE-947 | SFP Secondary Cluster: Authentication Bypass | category | Incomplete | taxonomy-only |  |
| CWE-948 | SFP Secondary Cluster: Digital Certificate | category | Incomplete | taxonomy-only |  |
| CWE-949 | SFP Secondary Cluster: Faulty Endpoint Authentication | category | Incomplete | taxonomy-only |  |
| CWE-950 | SFP Secondary Cluster: Hardcoded Sensitive Data | category | Incomplete | taxonomy-only |  |
| CWE-951 | SFP Secondary Cluster: Insecure Authentication Policy | category | Incomplete | taxonomy-only |  |
| CWE-952 | SFP Secondary Cluster: Missing Authentication | category | Incomplete | taxonomy-only |  |
| CWE-953 | SFP Secondary Cluster: Missing Endpoint Authentication | category | Incomplete | taxonomy-only |  |
| CWE-954 | SFP Secondary Cluster: Multiple Binds to the Same Port | category | Incomplete | taxonomy-only |  |
| CWE-955 | SFP Secondary Cluster: Unrestricted Authentication | category | Incomplete | taxonomy-only |  |
| CWE-956 | SFP Secondary Cluster: Channel Attack | category | Incomplete | taxonomy-only |  |
| CWE-957 | SFP Secondary Cluster: Protocol Error | category | Incomplete | taxonomy-only |  |
| CWE-958 | SFP Secondary Cluster: Broken Cryptography | category | Incomplete | taxonomy-only |  |
| CWE-959 | SFP Secondary Cluster: Weak Cryptography | category | Incomplete | taxonomy-only |  |
| CWE-960 | SFP Secondary Cluster: Ambiguous Exception Type | category | Incomplete | taxonomy-only |  |
| CWE-961 | SFP Secondary Cluster: Incorrect Exception Behavior | category | Incomplete | taxonomy-only |  |
| CWE-962 | SFP Secondary Cluster: Unchecked Status Condition | category | Incomplete | taxonomy-only |  |
| CWE-963 | SFP Secondary Cluster: Exposed Data | category | Incomplete | taxonomy-only |  |
| CWE-964 | SFP Secondary Cluster: Exposure Temporary File | category | Incomplete | taxonomy-only |  |
| CWE-965 | SFP Secondary Cluster: Insecure Session Management | category | Incomplete | taxonomy-only |  |
| CWE-966 | SFP Secondary Cluster: Other Exposures | category | Incomplete | taxonomy-only |  |
| CWE-967 | SFP Secondary Cluster: State Disclosure | category | Incomplete | taxonomy-only |  |
| CWE-968 | SFP Secondary Cluster: Covert Channel | category | Incomplete | taxonomy-only |  |
| CWE-969 | SFP Secondary Cluster: Faulty Memory Release | category | Incomplete | taxonomy-only |  |
| CWE-970 | SFP Secondary Cluster: Faulty Buffer Access | category | Incomplete | taxonomy-only |  |
| CWE-971 | SFP Secondary Cluster: Faulty Pointer Use | category | Incomplete | taxonomy-only |  |
| CWE-972 | SFP Secondary Cluster: Faulty String Expansion | category | Incomplete | taxonomy-only |  |
| CWE-973 | SFP Secondary Cluster: Improper NULL Termination | category | Incomplete | taxonomy-only |  |
| CWE-974 | SFP Secondary Cluster: Incorrect Buffer Length Computation | category | Incomplete | taxonomy-only |  |
| CWE-975 | SFP Secondary Cluster: Architecture | category | Incomplete | taxonomy-only |  |
| CWE-976 | SFP Secondary Cluster: Compiler | category | Incomplete | taxonomy-only |  |
| CWE-977 | SFP Secondary Cluster: Design | category | Incomplete | taxonomy-only |  |
| CWE-978 | SFP Secondary Cluster: Implementation | category | Incomplete | taxonomy-only |  |
| CWE-979 | SFP Secondary Cluster: Failed Chroot Jail | category | Incomplete | taxonomy-only |  |
| CWE-980 | SFP Secondary Cluster: Link in Resource Name Resolution | category | Incomplete | taxonomy-only |  |
| CWE-981 | SFP Secondary Cluster: Path Traversal | category | Incomplete | taxonomy-only |  |
| CWE-982 | SFP Secondary Cluster: Failure to Release Resource | category | Incomplete | taxonomy-only |  |
| CWE-983 | SFP Secondary Cluster: Faulty Resource Use | category | Incomplete | taxonomy-only |  |
| CWE-984 | SFP Secondary Cluster: Life Cycle | category | Incomplete | taxonomy-only |  |
| CWE-985 | SFP Secondary Cluster: Unrestricted Consumption | category | Incomplete | taxonomy-only |  |
| CWE-986 | SFP Secondary Cluster: Missing Lock | category | Incomplete | taxonomy-only |  |
| CWE-987 | SFP Secondary Cluster: Multiple Locks/Unlocks | category | Incomplete | taxonomy-only |  |
| CWE-988 | SFP Secondary Cluster: Race Condition Window | category | Incomplete | taxonomy-only |  |
| CWE-989 | SFP Secondary Cluster: Unrestricted Lock | category | Incomplete | taxonomy-only |  |
| CWE-990 | SFP Secondary Cluster: Tainted Input to Command | category | Incomplete | taxonomy-only |  |
| CWE-991 | SFP Secondary Cluster: Tainted Input to Environment | category | Incomplete | taxonomy-only |  |
| CWE-992 | SFP Secondary Cluster: Faulty Input Transformation | category | Incomplete | taxonomy-only |  |
| CWE-993 | SFP Secondary Cluster: Incorrect Input Handling | category | Incomplete | taxonomy-only |  |
| CWE-994 | SFP Secondary Cluster: Tainted Input to Variable | category | Incomplete | taxonomy-only |  |
| CWE-995 | SFP Secondary Cluster: Feature | category | Incomplete | taxonomy-only |  |
| CWE-996 | SFP Secondary Cluster: Security | category | Incomplete | taxonomy-only |  |
| CWE-997 | SFP Secondary Cluster: Information Loss | category | Incomplete | taxonomy-only |  |
| CWE-998 | SFP Secondary Cluster: Glitch in Computation | category | Incomplete | taxonomy-only |  |
| CWE-999 | DEPRECATED: Weaknesses without Software Fault Patterns | view | Deprecated | taxonomy-only |  |
| CWE-1000 | Research Concepts | view | Draft | taxonomy-only |  |
| CWE-1001 | SFP Secondary Cluster: Use of an Improper API | category | Incomplete | taxonomy-only |  |
| CWE-1002 | SFP Secondary Cluster: Unexpected Entry Points | category | Incomplete | taxonomy-only |  |
| CWE-1003 | Weaknesses for Simplified Mapping of Published Vulnerabilities | view | Incomplete | taxonomy-only |  |
| CWE-1004 | Sensitive Cookie Without 'HttpOnly' Flag | weakness | Incomplete | gap |  |
| CWE-1005 | 7PK - Input Validation and Representation | category | Draft | taxonomy-only |  |
| CWE-1006 | Bad Coding Practices | category | Draft | taxonomy-only |  |
| CWE-1007 | Insufficient Visual Distinction of Homoglyphs Presented to User | weakness | Incomplete | gap |  |
| CWE-1008 | Architectural Concepts | view | Incomplete | taxonomy-only |  |
| CWE-1009 | Audit | category | Draft | taxonomy-only |  |
| CWE-1010 | Authenticate Actors | category | Draft | taxonomy-only |  |
| CWE-1011 | Authorize Actors | category | Draft | taxonomy-only |  |
| CWE-1012 | Cross Cutting | category | Draft | taxonomy-only |  |
| CWE-1013 | Encrypt Data | category | Draft | taxonomy-only |  |
| CWE-1014 | Identify Actors | category | Draft | taxonomy-only |  |
| CWE-1015 | Limit Access | category | Draft | taxonomy-only |  |
| CWE-1016 | Limit Exposure | category | Draft | taxonomy-only |  |
| CWE-1017 | Lock Computer | category | Draft | taxonomy-only |  |
| CWE-1018 | Manage User Sessions | category | Draft | taxonomy-only |  |
| CWE-1019 | Validate Inputs | category | Draft | taxonomy-only |  |
| CWE-1020 | Verify Message Integrity | category | Draft | taxonomy-only |  |
| CWE-1021 | Improper Restriction of Rendered UI Layers or Frames | weakness | Incomplete | gap |  |
| CWE-1022 | Use of Web Link to Untrusted Target with window.opener Access | weakness | Incomplete | gap |  |
| CWE-1023 | Incomplete Comparison with Missing Factors | weakness | Incomplete | gap |  |
| CWE-1024 | Comparison of Incompatible Types | weakness | Incomplete | gap |  |
| CWE-1025 | Comparison Using Wrong Factors | weakness | Incomplete | gap |  |
| CWE-1026 | Weaknesses in OWASP Top Ten (2017) | view | Incomplete | taxonomy-only |  |
| CWE-1027 | OWASP Top Ten 2017 Category A1 - Injection | category | Incomplete | taxonomy-only |  |
| CWE-1028 | OWASP Top Ten 2017 Category A2 - Broken Authentication | category | Incomplete | taxonomy-only |  |
| CWE-1029 | OWASP Top Ten 2017 Category A3 - Sensitive Data Exposure | category | Incomplete | taxonomy-only |  |
| CWE-1030 | OWASP Top Ten 2017 Category A4 - XML External Entities (XXE) | category | Incomplete | taxonomy-only |  |
| CWE-1031 | OWASP Top Ten 2017 Category A5 - Broken Access Control | category | Incomplete | taxonomy-only |  |
| CWE-1032 | OWASP Top Ten 2017 Category A6 - Security Misconfiguration | category | Incomplete | taxonomy-only |  |
| CWE-1033 | OWASP Top Ten 2017 Category A7 - Cross-Site Scripting (XSS) | category | Incomplete | taxonomy-only |  |
| CWE-1034 | OWASP Top Ten 2017 Category A8 - Insecure Deserialization | category | Incomplete | taxonomy-only |  |
| CWE-1035 | OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities | category | Incomplete | taxonomy-only |  |
| CWE-1036 | OWASP Top Ten 2017 Category A10 - Insufficient Logging &amp; Monitoring | category | Incomplete | taxonomy-only |  |
| CWE-1037 | Processor Optimization Removal or Modification of Security-critical Code | weakness | Incomplete | gap |  |
| CWE-1038 | Insecure Automated Optimizations | weakness | Draft | gap |  |
| CWE-1039 | Inadequate Detection or Handling of Adversarial Input Perturbations in Automated Recognition Mechanism | weakness | Incomplete | gap |  |
| CWE-1040 | Quality Weaknesses with Indirect Security Impacts | view | Incomplete | taxonomy-only |  |
| CWE-1041 | Use of Redundant Code | weakness | Incomplete | gap |  |
| CWE-1042 | Static Member Data Element outside of a Singleton Class Element | weakness | Incomplete | gap |  |
| CWE-1043 | Data Element Aggregating an Excessively Large Number of Non-Primitive Elements | weakness | Incomplete | gap |  |
| CWE-1044 | Architecture with Number of Horizontal Layers Outside of Expected Range | weakness | Incomplete | gap |  |
| CWE-1045 | Parent Class with a Virtual Destructor and a Child Class without a Virtual Destructor | weakness | Incomplete | gap |  |
| CWE-1046 | Creation of Immutable Text Using String Concatenation | weakness | Incomplete | gap |  |
| CWE-1047 | Modules with Circular Dependencies | weakness | Incomplete | gap |  |
| CWE-1048 | Invokable Control Element with Large Number of Outward Calls | weakness | Incomplete | gap |  |
| CWE-1049 | Excessive Data Query Operations in a Large Data Table | weakness | Incomplete | gap |  |
| CWE-1050 | Excessive Platform Resource Consumption within a Loop | weakness | Incomplete | gap |  |
| CWE-1051 | Initialization with Hard-Coded Network Resource Configuration Data | weakness | Incomplete | gap |  |
| CWE-1052 | Excessive Use of Hard-Coded Literals in Initialization | weakness | Incomplete | gap |  |
| CWE-1053 | Missing Documentation for Design | weakness | Incomplete | gap |  |
| CWE-1054 | Invocation of a Control Element at an Unnecessarily Deep Horizontal Layer | weakness | Incomplete | gap |  |
| CWE-1055 | Multiple Inheritance from Concrete Classes | weakness | Incomplete | gap |  |
| CWE-1056 | Invokable Control Element with Variadic Parameters | weakness | Incomplete | gap |  |
| CWE-1057 | Data Access Operations Outside of Expected Data Manager Component | weakness | Incomplete | gap |  |
| CWE-1058 | Invokable Control Element in Multi-Thread Context with non-Final Static Storable or Member Element | weakness | Incomplete | gap |  |
| CWE-1059 | Insufficient Technical Documentation | weakness | Incomplete | gap |  |
| CWE-1060 | Excessive Number of Inefficient Server-Side Data Accesses | weakness | Incomplete | gap |  |
| CWE-1061 | Insufficient Encapsulation | weakness | Incomplete | gap |  |
| CWE-1062 | Parent Class with References to Child Class | weakness | Incomplete | gap |  |
| CWE-1063 | Creation of Class Instance within a Static Code Block | weakness | Incomplete | gap |  |
| CWE-1064 | Invokable Control Element with Signature Containing an Excessive Number of Parameters | weakness | Incomplete | gap |  |
| CWE-1065 | Runtime Resource Management Control Element in a Component Built to Run on Application Servers | weakness | Incomplete | gap |  |
| CWE-1066 | Missing Serialization Control Element | weakness | Incomplete | gap |  |
| CWE-1067 | Excessive Execution of Sequential Searches of Data Resource | weakness | Incomplete | gap |  |
| CWE-1068 | Inconsistency Between Implementation and Documented Design | weakness | Incomplete | gap |  |
| CWE-1069 | Empty Exception Block | weakness | Incomplete | gap |  |
| CWE-1070 | Serializable Data Element Containing non-Serializable Item Elements | weakness | Incomplete | gap |  |
| CWE-1071 | Empty Code Block | weakness | Incomplete | gap |  |
| CWE-1072 | Data Resource Access without Use of Connection Pooling | weakness | Incomplete | gap |  |
| CWE-1073 | Non-SQL Invokable Control Element with Excessive Number of Data Resource Accesses | weakness | Incomplete | gap |  |
| CWE-1074 | Class with Excessively Deep Inheritance | weakness | Incomplete | gap |  |
| CWE-1075 | Unconditional Control Flow Transfer outside of Switch Block | weakness | Incomplete | gap |  |
| CWE-1076 | Insufficient Adherence to Expected Conventions | weakness | Incomplete | gap |  |
| CWE-1077 | Floating Point Comparison with Incorrect Operator | weakness | Incomplete | gap |  |
| CWE-1078 | Inappropriate Source Code Style or Formatting | weakness | Incomplete | gap |  |
| CWE-1079 | Parent Class without Virtual Destructor Method | weakness | Incomplete | gap |  |
| CWE-1080 | Source Code File with Excessive Number of Lines of Code | weakness | Incomplete | gap |  |
| CWE-1081 | Entries with Maintenance Notes | view | Draft | taxonomy-only |  |
| CWE-1082 | Class Instance Self Destruction Control Element | weakness | Incomplete | gap |  |
| CWE-1083 | Data Access from Outside Expected Data Manager Component | weakness | Incomplete | gap |  |
| CWE-1084 | Invokable Control Element with Excessive File or Data Access Operations | weakness | Incomplete | gap |  |
| CWE-1085 | Invokable Control Element with Excessive Volume of Commented-out Code | weakness | Incomplete | gap |  |
| CWE-1086 | Class with Excessive Number of Child Classes | weakness | Incomplete | gap |  |
| CWE-1087 | Class with Virtual Method without a Virtual Destructor | weakness | Incomplete | gap |  |
| CWE-1088 | Synchronous Access of Remote Resource without Timeout | weakness | Incomplete | gap |  |
| CWE-1089 | Large Data Table with Excessive Number of Indices | weakness | Incomplete | gap |  |
| CWE-1090 | Method Containing Access of a Member Element from Another Class | weakness | Incomplete | gap |  |
| CWE-1091 | Use of Object without Invoking Destructor Method | weakness | Incomplete | gap |  |
| CWE-1092 | Use of Same Invokable Control Element in Multiple Architectural Layers | weakness | Incomplete | gap |  |
| CWE-1093 | Excessively Complex Data Representation | weakness | Incomplete | gap |  |
| CWE-1094 | Excessive Index Range Scan for a Data Resource | weakness | Incomplete | gap |  |
| CWE-1095 | Loop Condition Value Update within the Loop | weakness | Incomplete | gap |  |
| CWE-1096 | Singleton Class Instance Creation without Proper Locking or Synchronization | weakness | Incomplete | gap |  |
| CWE-1097 | Persistent Storable Data Element without Associated Comparison Control Element | weakness | Incomplete | gap |  |
| CWE-1098 | Data Element containing Pointer Item without Proper Copy Control Element | weakness | Incomplete | gap |  |
| CWE-1099 | Inconsistent Naming Conventions for Identifiers | weakness | Incomplete | gap |  |
| CWE-1100 | Insufficient Isolation of System-Dependent Functions | weakness | Incomplete | gap |  |
| CWE-1101 | Reliance on Runtime Component in Generated Code | weakness | Incomplete | gap |  |
| CWE-1102 | Reliance on Machine-Dependent Data Representation | weakness | Incomplete | gap |  |
| CWE-1103 | Use of Platform-Dependent Third Party Components | weakness | Incomplete | gap |  |
| CWE-1104 | Use of Unmaintained Third Party Components | weakness | Incomplete | gap |  |
| CWE-1105 | Insufficient Encapsulation of Machine-Dependent Functionality | weakness | Incomplete | gap |  |
| CWE-1106 | Insufficient Use of Symbolic Constants | weakness | Incomplete | gap |  |
| CWE-1107 | Insufficient Isolation of Symbolic Constant Definitions | weakness | Incomplete | gap |  |
| CWE-1108 | Excessive Reliance on Global Variables | weakness | Incomplete | gap |  |
| CWE-1109 | Use of Same Variable for Multiple Purposes | weakness | Incomplete | gap |  |
| CWE-1110 | Incomplete Design Documentation | weakness | Incomplete | gap |  |
| CWE-1111 | Incomplete I/O Documentation | weakness | Incomplete | gap |  |
| CWE-1112 | Incomplete Documentation of Program Execution | weakness | Incomplete | gap |  |
| CWE-1113 | Inappropriate Comment Style | weakness | Incomplete | gap |  |
| CWE-1114 | Inappropriate Whitespace Style | weakness | Incomplete | gap |  |
| CWE-1115 | Source Code Element without Standard Prologue | weakness | Incomplete | gap |  |
| CWE-1116 | Inaccurate Source Code Comments | weakness | Incomplete | gap |  |
| CWE-1117 | Callable with Insufficient Behavioral Summary | weakness | Incomplete | gap |  |
| CWE-1118 | Insufficient Documentation of Error Handling Techniques | weakness | Incomplete | gap |  |
| CWE-1119 | Excessive Use of Unconditional Branching | weakness | Incomplete | gap |  |
| CWE-1120 | Excessive Code Complexity | weakness | Incomplete | gap |  |
| CWE-1121 | Excessive McCabe Cyclomatic Complexity | weakness | Incomplete | gap |  |
| CWE-1122 | Excessive Halstead Complexity | weakness | Incomplete | gap |  |
| CWE-1123 | Excessive Use of Self-Modifying Code | weakness | Incomplete | gap |  |
| CWE-1124 | Excessively Deep Nesting | weakness | Incomplete | gap |  |
| CWE-1125 | Excessive Attack Surface | weakness | Incomplete | gap |  |
| CWE-1126 | Declaration of Variable with Unnecessarily Wide Scope | weakness | Incomplete | gap |  |
| CWE-1127 | Compilation with Insufficient Warnings or Errors | weakness | Incomplete | gap |  |
| CWE-1128 | CISQ Quality Measures (2016) | view | Incomplete | taxonomy-only |  |
| CWE-1129 | CISQ Quality Measures (2016) - Reliability | category | Draft | taxonomy-only |  |
| CWE-1130 | CISQ Quality Measures (2016) - Maintainability | category | Draft | taxonomy-only |  |
| CWE-1131 | CISQ Quality Measures (2016) - Security | category | Draft | taxonomy-only |  |
| CWE-1132 | CISQ Quality Measures (2016) - Performance Efficiency | category | Draft | taxonomy-only |  |
| CWE-1133 | Weaknesses Addressed by the SEI CERT Oracle Coding Standard for Java | view | Stable | taxonomy-only |  |
| CWE-1134 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 00. Input Validation and Data Sanitization (IDS) | category | Stable | taxonomy-only |  |
| CWE-1135 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 01. Declarations and Initialization (DCL) | category | Stable | taxonomy-only |  |
| CWE-1136 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 02. Expressions (EXP) | category | Stable | taxonomy-only |  |
| CWE-1137 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 03. Numeric Types and Operations (NUM) | category | Stable | taxonomy-only |  |
| CWE-1138 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 04. Characters and Strings (STR) | category | Stable | taxonomy-only |  |
| CWE-1139 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 05. Object Orientation (OBJ) | category | Stable | taxonomy-only |  |
| CWE-1140 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 06. Methods (MET) | category | Stable | taxonomy-only |  |
| CWE-1141 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 07. Exceptional Behavior (ERR) | category | Stable | taxonomy-only |  |
| CWE-1142 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 08. Visibility and Atomicity (VNA) | category | Stable | taxonomy-only |  |
| CWE-1143 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 09. Locking (LCK) | category | Stable | taxonomy-only |  |
| CWE-1144 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 10. Thread APIs (THI) | category | Stable | taxonomy-only |  |
| CWE-1145 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 11. Thread Pools (TPS) | category | Stable | taxonomy-only |  |
| CWE-1146 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 12. Thread-Safety Miscellaneous (TSM) | category | Stable | taxonomy-only |  |
| CWE-1147 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 13. Input Output (FIO) | category | Stable | taxonomy-only |  |
| CWE-1148 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 14. Serialization (SER) | category | Stable | taxonomy-only |  |
| CWE-1149 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 15. Platform Security (SEC) | category | Stable | taxonomy-only |  |
| CWE-1150 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 16. Runtime Environment (ENV) | category | Stable | taxonomy-only |  |
| CWE-1151 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 17. Java Native Interface (JNI) | category | Stable | taxonomy-only |  |
| CWE-1152 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 49. Miscellaneous (MSC) | category | Stable | taxonomy-only |  |
| CWE-1153 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 50. Android (DRD) | category | Stable | taxonomy-only |  |
| CWE-1154 | Weaknesses Addressed by the SEI CERT C Coding Standard | view | Stable | taxonomy-only |  |
| CWE-1155 | SEI CERT C Coding Standard - Guidelines 01. Preprocessor (PRE) | category | Stable | taxonomy-only |  |
| CWE-1156 | SEI CERT C Coding Standard - Guidelines 02. Declarations and Initialization (DCL) | category | Stable | taxonomy-only |  |
| CWE-1157 | SEI CERT C Coding Standard - Guidelines 03. Expressions (EXP) | category | Stable | taxonomy-only |  |
| CWE-1158 | SEI CERT C Coding Standard - Guidelines 04. Integers (INT) | category | Stable | taxonomy-only |  |
| CWE-1159 | SEI CERT C Coding Standard - Guidelines 05. Floating Point (FLP) | category | Stable | taxonomy-only |  |
| CWE-1160 | SEI CERT C Coding Standard - Guidelines 06. Arrays (ARR) | category | Stable | taxonomy-only |  |
| CWE-1161 | SEI CERT C Coding Standard - Guidelines 07. Characters and Strings (STR) | category | Stable | taxonomy-only |  |
| CWE-1162 | SEI CERT C Coding Standard - Guidelines 08. Memory Management (MEM) | category | Stable | taxonomy-only |  |
| CWE-1163 | SEI CERT C Coding Standard - Guidelines 09. Input Output (FIO) | category | Stable | taxonomy-only |  |
| CWE-1164 | Irrelevant Code | weakness | Incomplete | gap |  |
| CWE-1165 | SEI CERT C Coding Standard - Guidelines 10. Environment (ENV) | category | Stable | taxonomy-only |  |
| CWE-1166 | SEI CERT C Coding Standard - Guidelines 11. Signals (SIG) | category | Stable | taxonomy-only |  |
| CWE-1167 | SEI CERT C Coding Standard - Guidelines 12. Error Handling (ERR) | category | Stable | taxonomy-only |  |
| CWE-1168 | SEI CERT C Coding Standard - Guidelines 13. Application Programming Interfaces (API) | category | Stable | taxonomy-only |  |
| CWE-1169 | SEI CERT C Coding Standard - Guidelines 14. Concurrency (CON) | category | Stable | taxonomy-only |  |
| CWE-1170 | SEI CERT C Coding Standard - Guidelines 48. Miscellaneous (MSC) | category | Stable | taxonomy-only |  |
| CWE-1171 | SEI CERT C Coding Standard - Guidelines 50. POSIX (POS) | category | Stable | taxonomy-only |  |
| CWE-1172 | SEI CERT C Coding Standard - Guidelines 51. Microsoft Windows (WIN) | category | Stable | taxonomy-only |  |
| CWE-1173 | Improper Use of Validation Framework | weakness | Draft | gap |  |
| CWE-1174 | ASP.NET Misconfiguration: Improper Model Validation | weakness | Draft | gap |  |
| CWE-1175 | SEI CERT Oracle Secure Coding Standard for Java - Guidelines 18. Concurrency (CON) | category | Stable | taxonomy-only |  |
| CWE-1176 | Inefficient CPU Computation | weakness | Incomplete | gap |  |
| CWE-1177 | Use of Prohibited Code | weakness | Incomplete | gap |  |
| CWE-1178 | Weaknesses Addressed by the SEI CERT Perl Coding Standard | view | Stable | taxonomy-only |  |
| CWE-1179 | SEI CERT Perl Coding Standard - Guidelines 01. Input Validation and Data Sanitization (IDS) | category | Stable | taxonomy-only |  |
| CWE-1180 | SEI CERT Perl Coding Standard - Guidelines 02. Declarations and Initialization (DCL) | category | Stable | taxonomy-only |  |
| CWE-1181 | SEI CERT Perl Coding Standard - Guidelines 03. Expressions (EXP) | category | Stable | taxonomy-only |  |
| CWE-1182 | SEI CERT Perl Coding Standard - Guidelines 04. Integers (INT) | category | Stable | taxonomy-only |  |
| CWE-1183 | SEI CERT Perl Coding Standard - Guidelines 05. Strings (STR) | category | Stable | taxonomy-only |  |
| CWE-1184 | SEI CERT Perl Coding Standard - Guidelines 06. Object-Oriented Programming (OOP) | category | Stable | taxonomy-only |  |
| CWE-1185 | SEI CERT Perl Coding Standard - Guidelines 07. File Input and Output (FIO) | category | Stable | taxonomy-only |  |
| CWE-1186 | SEI CERT Perl Coding Standard - Guidelines 50. Miscellaneous (MSC) | category | Stable | taxonomy-only |  |
| CWE-1187 | DEPRECATED: Use of Uninitialized Resource | weakness | Deprecated | gap |  |
| CWE-1188 | Initialization of a Resource with an Insecure Default | weakness | Incomplete | gap |  |
| CWE-1189 | Improper Isolation of Shared Resources on System-on-a-Chip (SoC) | weakness | Stable | gap |  |
| CWE-1190 | DMA Device Enabled Too Early in Boot Phase | weakness | Draft | gap |  |
| CWE-1191 | On-Chip Debug and Test Interface With Improper Access Control | weakness | Stable | gap |  |
| CWE-1192 | Improper Identifier for IP Block used in System-On-Chip (SOC) | weakness | Draft | gap |  |
| CWE-1193 | Power-On of Untrusted Execution Core Before Enabling Fabric Access Control | weakness | Draft | gap |  |
| CWE-1194 | Hardware Design | view | Draft | taxonomy-only |  |
| CWE-1195 | Manufacturing and Life Cycle Management Concerns | category | Draft | taxonomy-only |  |
| CWE-1196 | Security Flow Issues | category | Draft | taxonomy-only |  |
| CWE-1197 | Integration Issues | category | Draft | taxonomy-only |  |
| CWE-1198 | Privilege Separation and Access Control Issues | category | Draft | taxonomy-only |  |
| CWE-1199 | General Circuit and Logic Design Concerns | category | Draft | taxonomy-only |  |
| CWE-1200 | Weaknesses in the 2019 CWE Top 25 Most Dangerous Software Errors | view | Stable | taxonomy-only |  |
| CWE-1201 | Core and Compute Issues | category | Draft | taxonomy-only |  |
| CWE-1202 | Memory and Storage Issues | category | Draft | taxonomy-only |  |
| CWE-1203 | Peripherals, On-chip Fabric, and Interface/IO Problems | category | Draft | taxonomy-only |  |
| CWE-1204 | Generation of Weak Initialization Vector (IV) | weakness | Incomplete | gap |  |
| CWE-1205 | Security Primitives and Cryptography Issues | category | Draft | taxonomy-only |  |
| CWE-1206 | Power, Clock, Thermal, and Reset Concerns | category | Draft | taxonomy-only |  |
| CWE-1207 | Debug and Test Problems | category | Draft | taxonomy-only |  |
| CWE-1208 | Cross-Cutting Problems | category | Draft | taxonomy-only |  |
| CWE-1209 | Failure to Disable Reserved Bits | weakness | Incomplete | gap |  |
| CWE-1210 | Audit / Logging Errors | category | Draft | taxonomy-only |  |
| CWE-1211 | Authentication Errors | category | Draft | taxonomy-only |  |
| CWE-1212 | Authorization Errors | category | Draft | taxonomy-only |  |
| CWE-1213 | Random Number Issues | category | Draft | taxonomy-only |  |
| CWE-1214 | Data Integrity Issues | category | Draft | taxonomy-only |  |
| CWE-1215 | Data Validation Issues | category | Draft | taxonomy-only |  |
| CWE-1216 | Lockout Mechanism Errors | category | Draft | taxonomy-only |  |
| CWE-1217 | User Session Errors | category | Draft | taxonomy-only |  |
| CWE-1218 | Memory Buffer Errors | category | Draft | taxonomy-only |  |
| CWE-1219 | File Handling Issues | category | Draft | taxonomy-only |  |
| CWE-1220 | Insufficient Granularity of Access Control | weakness | Incomplete | gap |  |
| CWE-1221 | Incorrect Register Defaults or Module Parameters | weakness | Incomplete | gap |  |
| CWE-1222 | Insufficient Granularity of Address Regions Protected by Register Locks | weakness | Incomplete | gap |  |
| CWE-1223 | Race Condition for Write-Once Attributes | weakness | Incomplete | gap |  |
| CWE-1224 | Improper Restriction of Write-Once Bit Fields | weakness | Incomplete | gap |  |
| CWE-1225 | Documentation Issues | category | Draft | taxonomy-only |  |
| CWE-1226 | Complexity Issues | category | Draft | taxonomy-only |  |
| CWE-1227 | Encapsulation Issues | category | Draft | taxonomy-only |  |
| CWE-1228 | API / Function Errors | category | Draft | taxonomy-only |  |
| CWE-1229 | Creation of Emergent Resource | weakness | Incomplete | gap |  |
| CWE-1230 | Exposure of Sensitive Information Through Metadata | weakness | Incomplete | gap |  |
| CWE-1231 | Improper Prevention of Lock Bit Modification | weakness | Stable | gap |  |
| CWE-1232 | Improper Lock Behavior After Power State Transition | weakness | Incomplete | gap |  |
| CWE-1233 | Security-Sensitive Hardware Controls with Missing Lock Bit Protection | weakness | Stable | gap |  |
| CWE-1234 | Hardware Internal or Debug Modes Allow Override of Locks | weakness | Incomplete | gap |  |
| CWE-1235 | Incorrect Use of Autoboxing and Unboxing for Performance Critical Operations | weakness | Incomplete | gap |  |
| CWE-1236 | Improper Neutralization of Formula Elements in a CSV File | weakness | Incomplete | implemented | [python/csv-formula-injection](../labs/python/csv-formula-injection/README.md) |
| CWE-1237 | SFP Primary Cluster: Faulty Resource Release | category | Incomplete | taxonomy-only |  |
| CWE-1238 | SFP Primary Cluster: Failure to Release Memory | category | Incomplete | taxonomy-only |  |
| CWE-1239 | Improper Zeroization of Hardware Register | weakness | Draft | gap |  |
| CWE-1240 | Use of a Cryptographic Primitive with a Risky Implementation | weakness | Draft | gap |  |
| CWE-1241 | Use of Predictable Algorithm in Random Number Generator | weakness | Draft | gap |  |
| CWE-1242 | Inclusion of Undocumented Features or Chicken Bits | weakness | Incomplete | gap |  |
| CWE-1243 | Sensitive Non-Volatile Information Not Protected During Debug | weakness | Incomplete | gap |  |
| CWE-1244 | Internal Asset Exposed to Unsafe Debug Access Level or State | weakness | Stable | gap |  |
| CWE-1245 | Improper Finite State Machines (FSMs) in Hardware Logic | weakness | Incomplete | gap |  |
| CWE-1246 | Improper Write Handling in Limited-write Non-Volatile Memories | weakness | Incomplete | gap |  |
| CWE-1247 | Improper Protection Against Voltage and Clock Glitches | weakness | Stable | gap |  |
| CWE-1248 | Semiconductor Defects in Hardware Logic with Security-Sensitive Implications | weakness | Incomplete | gap |  |
| CWE-1249 | Application-Level Admin Tool with Inconsistent View of Underlying Operating System | weakness | Incomplete | gap |  |
| CWE-1250 | Improper Preservation of Consistency Between Independent Representations of Shared State | weakness | Incomplete | gap |  |
| CWE-1251 | Mirrored Regions with Different Values | weakness | Incomplete | gap |  |
| CWE-1252 | CPU Hardware Not Configured to Support Exclusivity of Write and Execute Operations | weakness | Incomplete | gap |  |
| CWE-1253 | Incorrect Selection of Fuse Values | weakness | Draft | gap |  |
| CWE-1254 | Incorrect Comparison Logic Granularity | weakness | Draft | gap |  |
| CWE-1255 | Comparison Logic is Vulnerable to Power Side-Channel Attacks | weakness | Draft | gap |  |
| CWE-1256 | Improper Restriction of Software Interfaces to Hardware Features | weakness | Stable | gap |  |
| CWE-1257 | Improper Access Control Applied to Mirrored or Aliased Memory Regions | weakness | Incomplete | gap |  |
| CWE-1258 | Exposure of Sensitive System Information Due to Uncleared Debug Information | weakness | Draft | gap |  |
| CWE-1259 | Improper Restriction of Security Token Assignment | weakness | Incomplete | gap |  |
| CWE-1260 | Improper Handling of Overlap Between Protected Memory Ranges | weakness | Stable | gap |  |
| CWE-1261 | Improper Handling of Single Event Upsets | weakness | Draft | gap |  |
| CWE-1262 | Improper Access Control for Register Interface | weakness | Stable | gap |  |
| CWE-1263 | Improper Physical Access Control | weakness | Incomplete | gap |  |
| CWE-1264 | Hardware Logic with Insecure De-Synchronization between Control and Data Channels | weakness | Incomplete | gap |  |
| CWE-1265 | Unintended Reentrant Invocation of Non-reentrant Code Via Nested Calls | weakness | Draft | gap |  |
| CWE-1266 | Improper Scrubbing of Sensitive Data from Decommissioned Device | weakness | Incomplete | gap |  |
| CWE-1267 | Policy Uses Obsolete Encoding | weakness | Draft | gap |  |
| CWE-1268 | Policy Privileges are not Assigned Consistently Between Control and Data Agents | weakness | Draft | gap |  |
| CWE-1269 | Product Released in Non-Release Configuration | weakness | Incomplete | gap |  |
| CWE-1270 | Generation of Incorrect Security Tokens | weakness | Incomplete | gap |  |
| CWE-1271 | Uninitialized Value on Reset for Registers Holding Security Settings | weakness | Incomplete | gap |  |
| CWE-1272 | Sensitive Information Uncleared Before Debug/Power State Transition | weakness | Stable | gap |  |
| CWE-1273 | Device Unlock Credential Sharing | weakness | Incomplete | gap |  |
| CWE-1274 | Improper Access Control for Volatile Memory Containing Boot Code | weakness | Stable | gap |  |
| CWE-1275 | Sensitive Cookie with Improper SameSite Attribute | weakness | Incomplete | gap |  |
| CWE-1276 | Hardware Child Block Incorrectly Connected to Parent System | weakness | Incomplete | gap |  |
| CWE-1277 | Firmware Not Updateable | weakness | Draft | gap |  |
| CWE-1278 | Missing Protection Against Hardware Reverse Engineering Using Integrated Circuit (IC) Imaging Techniques | weakness | Incomplete | gap |  |
| CWE-1279 | Cryptographic Operations are run Before Supporting Units are Ready | weakness | Incomplete | gap |  |
| CWE-1280 | Access Control Check Implemented After Asset is Accessed | weakness | Incomplete | gap |  |
| CWE-1281 | Sequence of Processor Instructions Leads to Unexpected Behavior | weakness | Incomplete | gap |  |
| CWE-1282 | Assumed-Immutable Data is Stored in Writable Memory | weakness | Incomplete | gap |  |
| CWE-1283 | Mutable Attestation or Measurement Reporting Data | weakness | Incomplete | gap |  |
| CWE-1284 | Improper Validation of Specified Quantity in Input | weakness | Incomplete | implemented | [python/business-logic](../labs/python/business-logic/README.md), [cgi/business-logic](../labs/cgi/business-logic/README.md), [rest-api/business-logic](../labs/rest-api/business-logic/README.md), [ai/business-logic](../labs/ai/business-logic/README.md), [c/business-logic](../labs/c/business-logic/README.md), [cpp/business-logic](../labs/cpp/business-logic/README.md), [node/business-logic](../labs/node/business-logic/README.md), [typescript/business-logic](../labs/typescript/business-logic/README.md), [php/business-logic](../labs/php/business-logic/README.md), [ruby/business-logic](../labs/ruby/business-logic/README.md), [go/business-logic](../labs/go/business-logic/README.md), [java/business-logic](../labs/java/business-logic/README.md), [dotnet/business-logic](../labs/dotnet/business-logic/README.md), [rust/business-logic](../labs/rust/business-logic/README.md) |
| CWE-1285 | Improper Validation of Specified Index, Position, or Offset in Input | weakness | Incomplete | gap |  |
| CWE-1286 | Improper Validation of Syntactic Correctness of Input | weakness | Incomplete | gap |  |
| CWE-1287 | Improper Validation of Specified Type of Input | weakness | Incomplete | gap |  |
| CWE-1288 | Improper Validation of Consistency within Input | weakness | Incomplete | gap |  |
| CWE-1289 | Improper Validation of Unsafe Equivalence in Input | weakness | Incomplete | gap |  |
| CWE-1290 | Incorrect Decoding of Security Identifiers | weakness | Incomplete | gap |  |
| CWE-1291 | Public Key Re-Use for Signing both Debug and Production Code | weakness | Draft | gap |  |
| CWE-1292 | Incorrect Conversion of Security Identifiers | weakness | Draft | gap |  |
| CWE-1293 | Missing Source Correlation of Multiple Independent Data | weakness | Draft | gap |  |
| CWE-1294 | Insecure Security Identifier Mechanism | weakness | Incomplete | gap |  |
| CWE-1295 | Debug Messages Revealing Unnecessary Information | weakness | Incomplete | gap |  |
| CWE-1296 | Incorrect Chaining or Granularity of Debug Components | weakness | Incomplete | gap |  |
| CWE-1297 | Unprotected Confidential Information on Device is Accessible by OSAT Vendors | weakness | Incomplete | gap |  |
| CWE-1298 | Hardware Logic Contains Race Conditions | weakness | Draft | gap |  |
| CWE-1299 | Missing Protection Mechanism for Alternate Hardware Interface | weakness | Draft | gap |  |
| CWE-1300 | Improper Protection of Physical Side Channels | weakness | Stable | gap |  |
| CWE-1301 | Insufficient or Incomplete Data Removal within Hardware Component | weakness | Incomplete | gap |  |
| CWE-1302 | Missing Source Identifier in Entity Transactions on a System-On-Chip (SOC) | weakness | Incomplete | gap |  |
| CWE-1303 | Non-Transparent Sharing of Microarchitectural Resources | weakness | Draft | gap |  |
| CWE-1304 | Improperly Preserved Integrity of Hardware Configuration State During a Power Save/Restore Operation | weakness | Draft | gap |  |
| CWE-1305 | CISQ Quality Measures (2020) | view | Incomplete | taxonomy-only |  |
| CWE-1306 | CISQ Quality Measures - Reliability | category | Incomplete | taxonomy-only |  |
| CWE-1307 | CISQ Quality Measures - Maintainability | category | Incomplete | taxonomy-only |  |
| CWE-1308 | CISQ Quality Measures - Security | category | Incomplete | taxonomy-only |  |
| CWE-1309 | CISQ Quality Measures - Efficiency | category | Incomplete | taxonomy-only |  |
| CWE-1310 | Missing Ability to Patch ROM Code | weakness | Draft | gap |  |
| CWE-1311 | Improper Translation of Security Attributes by Fabric Bridge | weakness | Draft | gap |  |
| CWE-1312 | Missing Protection for Mirrored Regions in On-Chip Fabric Firewall | weakness | Draft | gap |  |
| CWE-1313 | Hardware Allows Activation of Test or Debug Logic at Runtime | weakness | Draft | gap |  |
| CWE-1314 | Missing Write Protection for Parametric Data Values | weakness | Draft | gap |  |
| CWE-1315 | Improper Setting of Bus Controlling Capability in Fabric End-point | weakness | Incomplete | gap |  |
| CWE-1316 | Fabric-Address Map Allows Programming of Unwarranted Overlaps of Protected and Unprotected Ranges | weakness | Draft | gap |  |
| CWE-1317 | Improper Access Control in Fabric Bridge | weakness | Draft | gap |  |
| CWE-1318 | Missing Support for Security Features in On-chip Fabrics or Buses | weakness | Incomplete | gap |  |
| CWE-1319 | Improper Protection against Electromagnetic Fault Injection (EM-FI) | weakness | Incomplete | gap |  |
| CWE-1320 | Improper Protection for Outbound Error Messages and Alert Signals | weakness | Draft | gap |  |
| CWE-1321 | Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution') | weakness | Incomplete | implemented | [node/prototype-pollution](../labs/node/prototype-pollution/README.md), [typescript/prototype-pollution](../labs/typescript/prototype-pollution/README.md) |
| CWE-1322 | Use of Blocking Code in Single-threaded, Non-blocking Context | weakness | Incomplete | gap |  |
| CWE-1323 | Improper Management of Sensitive Trace Data | weakness | Draft | gap |  |
| CWE-1324 | DEPRECATED: Sensitive Information Accessible by Physical Probing of JTAG Interface | weakness | Deprecated | gap |  |
| CWE-1325 | Improperly Controlled Sequential Memory Allocation | weakness | Incomplete | gap |  |
| CWE-1326 | Missing Immutable Root of Trust in Hardware | weakness | Draft | gap |  |
| CWE-1327 | Binding to an Unrestricted IP Address | weakness | Incomplete | gap |  |
| CWE-1328 | Security Version Number Mutable to Older Versions | weakness | Draft | gap |  |
| CWE-1329 | Reliance on Component That is Not Updateable | weakness | Incomplete | gap |  |
| CWE-1330 | Remanent Data Readable after Memory Erase | weakness | Draft | gap |  |
| CWE-1331 | Improper Isolation of Shared Resources in Network On Chip (NoC) | weakness | Stable | gap |  |
| CWE-1332 | Improper Handling of Faults that Lead to Instruction Skips | weakness | Stable | gap |  |
| CWE-1333 | Inefficient Regular Expression Complexity | weakness | Draft | gap |  |
| CWE-1334 | Unauthorized Error Injection Can Degrade Hardware Redundancy | weakness | Draft | gap |  |
| CWE-1335 | Incorrect Bitwise Shift of Integer | weakness | Draft | gap |  |
| CWE-1336 | Improper Neutralization of Special Elements Used in a Template Engine | weakness | Incomplete | gap |  |
| CWE-1337 | Weaknesses in the 2021 CWE Top 25 Most Dangerous Software Weaknesses | view | Stable | taxonomy-only |  |
| CWE-1338 | Improper Protections Against Hardware Overheating | weakness | Draft | gap |  |
| CWE-1339 | Insufficient Precision or Accuracy of a Real Number | weakness | Draft | gap |  |
| CWE-1340 | CISQ Data Protection Measures | view | Incomplete | taxonomy-only |  |
| CWE-1341 | Multiple Releases of Same Resource or Handle | weakness | Incomplete | gap |  |
| CWE-1342 | Information Exposure through Microarchitectural State after Transient Execution | weakness | Incomplete | gap |  |
| CWE-1343 | Weaknesses in the 2021 CWE Most Important Hardware Weaknesses List | view | Stable | taxonomy-only |  |
| CWE-1344 | Weaknesses in OWASP Top Ten (2021) | view | Incomplete | taxonomy-only |  |
| CWE-1345 | OWASP Top Ten 2021 Category A01:2021 - Broken Access Control | category | Incomplete | taxonomy-only |  |
| CWE-1346 | OWASP Top Ten 2021 Category A02:2021 - Cryptographic Failures | category | Incomplete | taxonomy-only |  |
| CWE-1347 | OWASP Top Ten 2021 Category A03:2021 - Injection | category | Incomplete | taxonomy-only |  |
| CWE-1348 | OWASP Top Ten 2021 Category A04:2021 - Insecure Design | category | Incomplete | taxonomy-only |  |
| CWE-1349 | OWASP Top Ten 2021 Category A05:2021 - Security Misconfiguration | category | Incomplete | taxonomy-only |  |
| CWE-1350 | Weaknesses in the 2020 CWE Top 25 Most Dangerous Software Weaknesses | view | Stable | taxonomy-only |  |
| CWE-1351 | Improper Handling of Hardware Behavior in Exceptionally Cold Environments | weakness | Incomplete | gap |  |
| CWE-1352 | OWASP Top Ten 2021 Category A06:2021 - Vulnerable and Outdated Components | category | Incomplete | taxonomy-only |  |
| CWE-1353 | OWASP Top Ten 2021 Category A07:2021 - Identification and Authentication Failures | category | Incomplete | taxonomy-only |  |
| CWE-1354 | OWASP Top Ten 2021 Category A08:2021 - Software and Data Integrity Failures | category | Incomplete | taxonomy-only |  |
| CWE-1355 | OWASP Top Ten 2021 Category A09:2021 - Security Logging and Monitoring Failures | category | Incomplete | taxonomy-only |  |
| CWE-1356 | OWASP Top Ten 2021 Category A10:2021 - Server-Side Request Forgery (SSRF) | category | Incomplete | taxonomy-only |  |
| CWE-1357 | Reliance on Insufficiently Trustworthy Component | weakness | Incomplete | gap |  |
| CWE-1358 | Weaknesses in SEI ETF Categories of Security Vulnerabilities in ICS | view | Incomplete | taxonomy-only |  |
| CWE-1359 | ICS Communications | category | Incomplete | taxonomy-only |  |
| CWE-1360 | ICS Dependencies (&amp; Architecture) | category | Incomplete | taxonomy-only |  |
| CWE-1361 | ICS Supply Chain | category | Incomplete | taxonomy-only |  |
| CWE-1362 | ICS Engineering (Constructions/Deployment) | category | Incomplete | taxonomy-only |  |
| CWE-1363 | ICS Operations (&amp; Maintenance) | category | Incomplete | taxonomy-only |  |
| CWE-1364 | ICS Communications: Zone Boundary Failures | category | Incomplete | taxonomy-only |  |
| CWE-1365 | ICS Communications: Unreliability | category | Incomplete | taxonomy-only |  |
| CWE-1366 | ICS Communications: Frail Security in Protocols | category | Incomplete | taxonomy-only |  |
| CWE-1367 | ICS Dependencies (&amp; Architecture): External Physical Systems | category | Incomplete | taxonomy-only |  |
| CWE-1368 | ICS Dependencies (&amp; Architecture): External Digital Systems | category | Incomplete | taxonomy-only |  |
| CWE-1369 | ICS Supply Chain: IT/OT Convergence/Expansion | category | Incomplete | taxonomy-only |  |
| CWE-1370 | ICS Supply Chain: Common Mode Frailties | category | Incomplete | taxonomy-only |  |
| CWE-1371 | ICS Supply Chain: Poorly Documented or Undocumented Features | category | Incomplete | taxonomy-only |  |
| CWE-1372 | ICS Supply Chain: OT Counterfeit and Malicious Corruption | category | Incomplete | taxonomy-only |  |
| CWE-1373 | ICS Engineering (Construction/Deployment): Trust Model Problems | category | Incomplete | taxonomy-only |  |
| CWE-1374 | ICS Engineering (Construction/Deployment): Maker Breaker Blindness | category | Incomplete | taxonomy-only |  |
| CWE-1375 | ICS Engineering (Construction/Deployment): Gaps in Details/Data | category | Incomplete | taxonomy-only |  |
| CWE-1376 | ICS Engineering (Construction/Deployment): Security Gaps in Commissioning | category | Incomplete | taxonomy-only |  |
| CWE-1377 | ICS Engineering (Construction/Deployment): Inherent Predictability in Design | category | Incomplete | taxonomy-only |  |
| CWE-1378 | ICS Operations (&amp; Maintenance): Gaps in obligations and training | category | Incomplete | taxonomy-only |  |
| CWE-1379 | ICS Operations (&amp; Maintenance): Human factors in ICS environments | category | Incomplete | taxonomy-only |  |
| CWE-1380 | ICS Operations (&amp; Maintenance): Post-analysis changes | category | Incomplete | taxonomy-only |  |
| CWE-1381 | ICS Operations (&amp; Maintenance): Exploitable Standard Operational Procedures | category | Incomplete | taxonomy-only |  |
| CWE-1382 | ICS Operations (&amp; Maintenance): Emerging Energy Technologies | category | Incomplete | taxonomy-only |  |
| CWE-1383 | ICS Operations (&amp; Maintenance): Compliance/Conformance with Regulatory Requirements | category | Incomplete | taxonomy-only |  |
| CWE-1384 | Improper Handling of Physical or Environmental Conditions | weakness | Incomplete | gap |  |
| CWE-1385 | Missing Origin Validation in WebSockets | weakness | Incomplete | gap |  |
| CWE-1386 | Insecure Operation on Windows Junction / Mount Point | weakness | Incomplete | gap |  |
| CWE-1387 | Weaknesses in the 2022 CWE Top 25 Most Dangerous Software Weaknesses | view | Draft | taxonomy-only |  |
| CWE-1388 | Physical Access Issues and Concerns | category | Draft | taxonomy-only |  |
| CWE-1389 | Incorrect Parsing of Numbers with Different Radices | weakness | Incomplete | gap |  |
| CWE-1390 | Weak Authentication | weakness | Incomplete | gap |  |
| CWE-1391 | Use of Weak Credentials | weakness | Incomplete | gap |  |
| CWE-1392 | Use of Default Credentials | weakness | Incomplete | gap |  |
| CWE-1393 | Use of Default Password | weakness | Incomplete | gap |  |
| CWE-1394 | Use of Default Cryptographic Key | weakness | Incomplete | gap |  |
| CWE-1395 | Dependency on Vulnerable Third-Party Component | weakness | Incomplete | implemented | [node/vulnerable-dependency](../labs/node/vulnerable-dependency/README.md), [node/vulnerable-transitive-dependency](../labs/node/vulnerable-transitive-dependency/README.md) |
| CWE-1396 | Comprehensive Categorization: Access Control | category | Incomplete | taxonomy-only |  |
| CWE-1397 | Comprehensive Categorization: Comparison | category | Incomplete | taxonomy-only |  |
| CWE-1398 | Comprehensive Categorization: Component Interaction | category | Incomplete | taxonomy-only |  |
| CWE-1399 | Comprehensive Categorization: Memory Safety | category | Incomplete | taxonomy-only |  |
| CWE-1400 | Comprehensive Categorization for Software Assurance Trends | view | Draft | taxonomy-only |  |
| CWE-1401 | Comprehensive Categorization: Concurrency | category | Incomplete | taxonomy-only |  |
| CWE-1402 | Comprehensive Categorization: Encryption | category | Incomplete | taxonomy-only |  |
| CWE-1403 | Comprehensive Categorization: Exposed Resource | category | Incomplete | taxonomy-only |  |
| CWE-1404 | Comprehensive Categorization: File Handling | category | Incomplete | taxonomy-only |  |
| CWE-1405 | Comprehensive Categorization: Improper Check or Handling of Exceptional Conditions | category | Incomplete | taxonomy-only |  |
| CWE-1406 | Comprehensive Categorization: Improper Input Validation | category | Incomplete | taxonomy-only |  |
| CWE-1407 | Comprehensive Categorization: Improper Neutralization | category | Incomplete | taxonomy-only |  |
| CWE-1408 | Comprehensive Categorization: Incorrect Calculation | category | Incomplete | taxonomy-only |  |
| CWE-1409 | Comprehensive Categorization: Injection | category | Incomplete | taxonomy-only |  |
| CWE-1410 | Comprehensive Categorization: Insufficient Control Flow Management | category | Incomplete | taxonomy-only |  |
| CWE-1411 | Comprehensive Categorization: Insufficient Verification of Data Authenticity | category | Incomplete | taxonomy-only |  |
| CWE-1412 | Comprehensive Categorization: Poor Coding Practices | category | Incomplete | taxonomy-only |  |
| CWE-1413 | Comprehensive Categorization: Protection Mechanism Failure | category | Incomplete | taxonomy-only |  |
| CWE-1414 | Comprehensive Categorization: Randomness | category | Incomplete | taxonomy-only |  |
| CWE-1415 | Comprehensive Categorization: Resource Control | category | Incomplete | taxonomy-only |  |
| CWE-1416 | Comprehensive Categorization: Resource Lifecycle Management | category | Incomplete | taxonomy-only |  |
| CWE-1417 | Comprehensive Categorization: Sensitive Information Exposure | category | Incomplete | taxonomy-only |  |
| CWE-1418 | Comprehensive Categorization: Violation of Secure Design Principles | category | Incomplete | taxonomy-only |  |
| CWE-1419 | Incorrect Initialization of Resource | weakness | Incomplete | gap |  |
| CWE-1420 | Exposure of Sensitive Information during Transient Execution | weakness | Incomplete | gap |  |
| CWE-1421 | Exposure of Sensitive Information in Shared Microarchitectural Structures during Transient Execution | weakness | Incomplete | gap |  |
| CWE-1422 | Exposure of Sensitive Information caused by Incorrect Data Forwarding during Transient Execution | weakness | Incomplete | gap |  |
| CWE-1423 | Exposure of Sensitive Information caused by Shared Microarchitectural Predictor State that Influences Transient Execution | weakness | Incomplete | gap |  |
| CWE-1424 | Weaknesses Addressed by ISA/IEC 62443 Requirements | view | Draft | taxonomy-only |  |
| CWE-1425 | Weaknesses in the 2023 CWE Top 25 Most Dangerous Software Weaknesses | view | Draft | taxonomy-only |  |
| CWE-1426 | Improper Validation of Generative AI Output | weakness | Incomplete | gap |  |
| CWE-1427 | Improper Neutralization of Input Used for LLM Prompting | weakness | Incomplete | implemented | [ai/prompt-trust-boundary](../labs/ai/prompt-trust-boundary/README.md) |
| CWE-1428 | Reliance on HTTP instead of HTTPS | weakness | Incomplete | gap |  |
| CWE-1429 | Missing Security-Relevant Feedback for Unexecuted Operations in Hardware Interface | weakness | Incomplete | gap |  |
| CWE-1430 | Weaknesses in the 2024 CWE Top 25 Most Dangerous Software Weaknesses | view | Draft | taxonomy-only |  |
| CWE-1431 | Driving Intermediate Cryptographic State/Results to Hardware Module Outputs | weakness | Incomplete | gap |  |
| CWE-1432 | Weaknesses in the 2025 CWE Most Important Hardware Weaknesses List | view | Stable | taxonomy-only |  |
| CWE-1433 | 2025 MIHW Supplement: Expert Insights | category | Obsolete | taxonomy-only |  |
| CWE-1434 | Insecure Setting of Generative AI/ML Model Inference Parameters | weakness | Draft | gap |  |
| CWE-1435 | Weaknesses in the 2025 CWE Top 25 Most Dangerous Software Weaknesses | view | Draft | taxonomy-only |  |
| CWE-1436 | OWASP Top Ten 2025 Category A01:2025 - Broken Access Control | category | Incomplete | taxonomy-only |  |
| CWE-1437 | OWASP Top Ten 2025 Category A02:2025 - Security Misconfiguration | category | Incomplete | taxonomy-only |  |
| CWE-1438 | OWASP Top Ten 2025 Category A03:2025 - Software Supply Chain Failures | category | Incomplete | taxonomy-only |  |
| CWE-1439 | OWASP Top Ten 2025 Category A04:2025 - Cryptographic Failures | category | Incomplete | taxonomy-only |  |
| CWE-1440 | OWASP Top Ten 2025 Category A05:2025 - Injection | category | Incomplete | taxonomy-only |  |
| CWE-1441 | OWASP Top Ten 2025 Category A06:2025 - Insecure Design | category | Incomplete | taxonomy-only |  |
| CWE-1442 | OWASP Top Ten 2025 Category A07:2025 - Authentication Failures | category | Incomplete | taxonomy-only |  |
| CWE-1443 | OWASP Top Ten 2025 Category A08:2025 - Software or Data Integrity Failures | category | Incomplete | taxonomy-only |  |
| CWE-1444 | OWASP Top Ten 2025 Category A09:2025 - Logging &amp; Alerting Failures | category | Incomplete | taxonomy-only |  |
| CWE-1445 | OWASP Top Ten 2025 Category A10:2025 - Mishandling of Exceptional Conditions | category | Incomplete | taxonomy-only |  |
| CWE-1446 | Weaknesses That are Specific to AI/ML Technology | category | Incomplete | taxonomy-only |  |
| CWE-1447 | General Software Weaknesses that Appear in Products that Use or Support AI/ML Technology | category | Incomplete | taxonomy-only |  |
| CWE-1448 | Weaknesses Related to AI/ML Products | view | Incomplete | taxonomy-only |  |
| CWE-1450 | Weaknesses in OWASP Top Ten RC1 (2025) | view | Incomplete | taxonomy-only |  |
| CWE-2000 | Comprehensive CWE Dictionary | view | Draft | taxonomy-only |  |
