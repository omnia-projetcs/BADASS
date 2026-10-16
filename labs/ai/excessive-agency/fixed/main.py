def run(call):
    # This audit task has read-only capabilities established by the operator.
    allowed = {'read_source', 'report_finding'}
    if call['tool'] not in allowed:
        return 'DENIED'
    return 'EXECUTED:' + call['tool']
