# ============================================================
# HIT137 - Assignment 2 | S1 2026
# Question 2: Mathematical Expression Evaluator
# File: evaluator.py
#
# Requirements:
#   - Plain functions only, NO classes
#   - Recursive descent parsing (one function per precedence level)
#   - Handles: +, -, *, /, parentheses, unary negation
#   - Unary + produces ERROR
#   - Implicit multiplication supported
#   - Terminal AND output.txt both print same 4-line block format
# ============================================================

import os


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


# ─────────────────────────────────────────────────────────────
# STEP 4 — RESULT FORMATTING
# ─────────────────────────────────────────────────────────────

def format_result(value):
    """Whole numbers -> no decimal. Decimals -> 4 decimal places."""
    if value == int(value):
        return str(int(value))
    return f'{value:.4f}'


# ─────────────────────────────────────────────────────────────
# STEP 5 — PRINT ONE BLOCK TO TERMINAL
# ─────────────────────────────────────────────────────────────

def print_block(entry, result_str, last=False):
    """Print 4-line block to terminal. Blank line after unless last."""
    print(f"Input: {entry['input']}")
    print(f"Tree: {entry['tree']}")
    print(f"Tokens: {entry['tokens']}")
    print(f"Result: {result_str}")
    if not last:
        print()


# ─────────────────────────────────────────────────────────────
# STEP 6 — MAIN INTERFACE (required by assignment)
# ─────────────────────────────────────────────────────────────

def evaluate_file(input_path: str) -> list[dict]:
    """
    Read expressions from input_path, evaluate each one,
    print 4-line blocks to terminal, and write output.txt.

    Returns list of dicts:
        {"input": str, "tree": str, "tokens": str, "result": float|"ERROR"}
    """
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(input_path)), "output.txt"
    )

    with open(input_path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n\r") for line in f.readlines()]

    results   = []
    out_lines = []

    for idx, expr in enumerate(lines):
        entry = {
            "input":  expr,
            "tree":   "ERROR",
            "tokens": "ERROR",
            "result": "ERROR"
        }
        result_str = "ERROR"

        try:
            tokens    = tokenise(expr)
            token_str = format_tokens(tokens)
            tree      = parse(tokens)
            tree_s    = tree_str(tree)
            value     = eval_node(tree)

            entry["tokens"] = token_str
            entry["tree"]   = tree_s
            entry["result"] = value
            result_str      = format_result(value)

        except ZeroDivisionError:
            try:
                tokens    = tokenise(expr)
                token_str = format_tokens(tokens)
                tree      = parse(tokens)
                tree_s    = tree_str(tree)
                entry["tokens"] = token_str
                entry["tree"]   = tree_s
            except Exception:
                pass

        except Exception:
            try:
                tokens    = tokenise(expr)
                token_str = format_tokens(tokens)
                entry["tokens"] = token_str
            except Exception:
                pass

        # Print to terminal in required 4-line format
        is_last = (idx == len(lines) - 1)
        print_block(entry, result_str, last=is_last)

        # Write to output.txt
        out_lines.append(f"Input: {entry['input']}")
        out_lines.append(f"Tree: {entry['tree']}")
        out_lines.append(f"Tokens: {entry['tokens']}")
        out_lines.append(f"Result: {result_str}")
        out_lines.append("")

        results.append(entry)

    if out_lines and out_lines[-1] == "":
        out_lines.pop()

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(out_lines))

    return results


# ─────────────────────────────────────────────────────────────
# Run: python evaluator.py sample_input.txt
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "sample_input.txt"
    evaluate_file(path)