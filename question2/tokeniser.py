# ============================================================
# HIT137 - Assignment 2 | S1 2026
# Question 2: Tokeniser + Parse Tree Helpers + Parser
# File: tokeniser.py
# Author: Nisham
# ============================================================

# ─────────────────────────────────────────────────────────────
# STEP 1 — TOKENISER
# ─────────────────────────────────────────────────────────────

def tokenise(expr):
    """Split expression string into list of (TYPE, value) tokens."""
    tokens = []
    i = 0

    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1

        elif ch in ('+', '-', '*', '/'):
            tokens.append(('OP', ch))
            i += 1

        elif ch == '(':
            tokens.append(('LPAREN', '('))
            i += 1

        elif ch == ')':
            tokens.append(('RPAREN', ')'))
            i += 1

        elif ch.isdigit() or (ch == '.' and i + 1 < len(expr) and expr[i+1].isdigit()):
            j = i
            while j < len(expr) and (expr[j].isdigit() or expr[j] == '.'):
                j += 1
            tokens.append(('NUM', expr[i:j]))
            i = j

        else:
            raise ValueError(f"Unknown character: {repr(ch)}")

    tokens.append(('END', 'END'))
    return tokens


def format_tokens(tokens):
    """Format tokens as [TYPE:value] blocks. END shown as [END] only."""
    parts = []
    for t, v in tokens:
        if t == 'END':
            parts.append('[END]')
        else:
            parts.append(f'[{t}:{v}]')
    return ' '.join(parts)


# ─────────────────────────────────────────────────────────────
# STEP 2 — PARSE TREE HELPERS
# ─────────────────────────────────────────────────────────────

def tree_str(node):
    """
    Recursively convert parse tree to required string form.
    BASE CASE:  NUM   -> return number as string
    RECURSIVE:  BINOP -> "(op left right)"
    RECURSIVE:  NEG   -> "(neg operand)"
    """
    kind = node[0]

    if kind == 'NUM':                               # BASE CASE
        v = node[1]
        return str(int(v)) if v == int(v) else f'{v:.10g}'

    elif kind == 'BINOP':                           # RECURSIVE CASE
        _, op, left, right = node
        return f'({op} {tree_str(left)} {tree_str(right)})'

    elif kind == 'NEG':                             # RECURSIVE CASE
        return f'(neg {tree_str(node[1])})'


def eval_node(node):
    """
    Recursively evaluate parse tree and return numeric result.
    BASE CASE:  NUM   -> return the number
    RECURSIVE:  NEG   -> return negated result
    RECURSIVE:  BINOP -> return computed result
    Raises ZeroDivisionError for division by zero.
    """
    kind = node[0]

    if kind == 'NUM':                               # BASE CASE
        return node[1]

    elif kind == 'NEG':                             # RECURSIVE CASE
        return -eval_node(node[1])

    elif kind == 'BINOP':                           # RECURSIVE CASE
        _, op, left, right = node
        lv = eval_node(left)
        rv = eval_node(right)

        if op == '+':   return lv + rv
        elif op == '-': return lv - rv
        elif op == '*': return lv * rv
        elif op == '/':
            if rv == 0:
                raise ZeroDivisionError("division by zero")
            return lv / rv


# ─────────────────────────────────────────────────────────────
# STEP 3 — RECURSIVE DESCENT PARSER (NO classes)
# ─────────────────────────────────────────────────────────────

def parse_expr(tokens, pos):
    """
    Handle + and - (lowest precedence).
    BASE CASE:  no + or - -> return left
    RECURSIVE:  consume + or -, build BINOP, repeat
    """
    left = parse_term(tokens, pos)

    while tokens[pos[0]][0] == 'OP' and tokens[pos[0]][1] in ('+', '-'):
        op = tokens[pos[0]][1]
        pos[0] += 1
        right = parse_term(tokens, pos)
        left = ('BINOP', op, left, right)

    return left


def parse_term(tokens, pos):
    """
    Handle * and / and implicit multiplication.
    BASE CASE:  no * / or implicit mult -> return left
    RECURSIVE:  consume operator, build BINOP, repeat
    """
    left = parse_unary(tokens, pos)

    while True:
        tok_type, tok_val = tokens[pos[0]]

        if tok_type == 'OP' and tok_val in ('*', '/'):
            op = tok_val
            pos[0] += 1
            right = parse_unary(tokens, pos)
            left = ('BINOP', op, left, right)

        elif tok_type in ('NUM', 'LPAREN'):
            right = parse_unary(tokens, pos)
            left = ('BINOP', '*', left, right)

        else:
            break                                   # BASE CASE

    return left


def parse_unary(tokens, pos):
    """
    Handle unary negation: -x, --x, -(expr).
    BASE CASE:  no minus -> go to parse_primary
    RECURSIVE:  minus found -> consume, recurse
    """
    tok_type, tok_val = tokens[pos[0]]

    if tok_type == 'OP' and tok_val == '-':         # RECURSIVE CASE
        pos[0] += 1
        operand = parse_unary(tokens, pos)
        return ('NEG', operand)

    if tok_type == 'OP' and tok_val == '+':
        raise SyntaxError("Unary + is not supported")

    return parse_primary(tokens, pos)               # BASE CASE


def parse_primary(tokens, pos):
    """
    Handle numbers and parenthesised sub-expressions (highest precedence).
    BASE CASE:  number -> return NUM node
    RECURSIVE:  ( -> parse inner expr -> expect ) -> return node
    """
    tok_type, tok_val = tokens[pos[0]]

    if tok_type == 'NUM':                           # BASE CASE
        pos[0] += 1
        return ('NUM', float(tok_val))

    elif tok_type == 'LPAREN':                      # RECURSIVE CASE
        pos[0] += 1
        node = parse_expr(tokens, pos)
        if tokens[pos[0]][0] != 'RPAREN':
            raise SyntaxError("Expected closing parenthesis ')'")
        pos[0] += 1
        return node

    else:
        raise SyntaxError(f"Unexpected token: {tokens[pos[0]]}")


def parse(tokens):
    """Entry point: parse full token list, return root tree node."""
    pos = [0]
    node = parse_expr(tokens, pos)
    if tokens[pos[0]][0] != 'END':
        raise SyntaxError(f"Unexpected token: {tokens[pos[0]]}")
    return node