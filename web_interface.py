#!/usr/bin/env python3
"""
MiniC Compiler Web Interface
A simple Flask-based web interface to demonstrate the MiniC compiler
"""

from flask import Flask, render_template, request, jsonify
import os
import sys

# Add compiler to path
sys.path.insert(0, os.path.dirname(__file__))

from compiler.lexer import lex, LexerError
from compiler.parser import parse, ParseError
from compiler.semantic import analyze, SemanticError
from compiler.ir_generator import generate_ir, print_ir
from compiler.optimizer import optimize
from compiler.asmgen import AssemblyGenerator
from compiler.ast_nodes import print_ast

app = Flask(__name__)

def compile_code(source_code):
    """Compile MiniC code and return all phases"""
    result = {
        'success': False,
        'tokens': '',
        'ast': '',
        'semantic': '',
        'ir': '',
        'optimized_ir': '',
        'assembly': '',
        'error': ''
    }
    
    try:
        # Phase 1: Lexical Analysis
        tokens = lex(source_code)
        
        # Group tokens by type
        from collections import defaultdict
        token_groups = defaultdict(list)
        for idx, token in enumerate(tokens, 1):
            token_groups[token.type.name].append((idx, token))
        
        # Format tokens in separate tables by type
        token_output = []
        
        # Define category order for better organization
        token_categories = {
            'Keywords': ['INT', 'BOOL', 'IF', 'ELSE', 'WHILE', 'PRINT', 'TRUE', 'FALSE'],
            'Identifiers & Literals': ['IDENTIFIER', 'NUMBER'],
            'Operators': ['PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE', 'MODULO', 'ASSIGN'],
            'Comparison Operators': ['LESS_THAN', 'GREATER_THAN', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL', 'NOT_EQUAL'],
            'Logical Operators': ['AND', 'OR', 'NOT'],
            'Delimiters': ['SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE'],
            'Other': ['EOF']
        }
        
        for category, token_types in token_categories.items():
            category_tokens = []
            for token_type in token_types:
                if token_type in token_groups:
                    category_tokens.extend(token_groups[token_type])
            
            if category_tokens:
                token_output.append(f"\n{category}:")
                token_output.append("=" * 80)
                token_output.append(f"{'No.':<6} {'Type':<20} {'Value':<20} {'Line':<8} {'Column':<8}")
                token_output.append("-" * 80)
                
                for idx, token in category_tokens:
                    token_type = token.type.name
                    token_value = token.value if len(token.value) <= 18 else token.value[:15] + "..."
                    token_output.append(f"{idx:<6} {token_type:<20} {token_value:<20} {token.line:<8} {token.column:<8}")
        
        result['tokens'] = '\n'.join(token_output)
        
        # Phase 2: Syntax Analysis
        ast = parse(tokens)
        result['ast'] = print_ast(ast)
        
        # Phase 3: Semantic Analysis
        from compiler.semantic import SemanticAnalyzer
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Get symbol table from analyzer
        symbol_info = []
        for name, var_type in analyzer.symbol_table.symbols.items():
            symbol_info.append(f"  {name}: {var_type}")
        
        result['semantic'] = "✓ Semantic Analysis Passed\n\n"
        if symbol_info:
            result['semantic'] += "Symbol Table:\n" + "\n".join(symbol_info)
        else:
            result['semantic'] += "No variables declared."
        
        # Phase 4: IR Generation
        ir_instructions = generate_ir(ast)
        result['ir'] = print_ir(ir_instructions)
        
        # Phase 5: Optimization
        optimized = optimize(ir_instructions)
        result['optimized_ir'] = print_ir(optimized)
        
        # Phase 6: Assembly Generation
        asm_gen = AssemblyGenerator()
        assembly = asm_gen.generate(optimized)
        result['assembly'] = assembly
        
        result['success'] = True
        
    except (LexerError, ParseError, SemanticError) as e:
        result['error'] = str(e)
    except Exception as e:
        result['error'] = f"Compiler error: {str(e)}"
    
    return result

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/compile', methods=['POST'])
def compile_endpoint():
    """Compile endpoint"""
    data = request.get_json()
    source_code = data.get('code', '')
    
    result = compile_code(source_code)
    return jsonify(result)

@app.route('/examples')
def get_examples():
    """Get list of example programs"""
    examples_dir = os.path.join(os.path.dirname(__file__), 'examples')
    examples = {}
    
    for filename in os.listdir(examples_dir):
        if filename.endswith('.mc'):
            filepath = os.path.join(examples_dir, filename)
            with open(filepath, 'r') as f:
                examples[filename] = f.read()
    
    return jsonify(examples)

if __name__ == '__main__':
    print("=" * 70)
    print("MiniC Compiler Web Interface")
    print("=" * 70)
    print("\nStarting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
