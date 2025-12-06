#!/usr/bin/env python3
"""
MiniC Compiler - Main Entry Point

A complete compiler for the MiniC programming language demonstrating
all six classical compiler phases. Generates x86-64 assembly code.

Usage:
    python minic.py <input_file.mc> [-o <output_file.s>] [options]

Options:
    -o, --output FILE       Output assembly file (default: output.s)
    --show-tokens          Display lexer tokens
    --show-ast             Display Abstract Syntax Tree
    --show-ir              Display Three-Address Code (IR)
    --show-asm             Display generated assembly code
    --no-optimize          Disable optimizations
    -h, --help             Show this help message
"""

import sys
import argparse
from pathlib import Path

# Import compiler modules
from compiler.lexer import lex, LexerError
from compiler.parser import parse, ParseError
from compiler.semantic import analyze, SemanticError
from compiler.ir_generator import generate_ir, print_ir
from compiler.optimizer import optimize
from compiler.asmgen import AssemblyGenerator
from compiler.ast_nodes import print_ast


class CompilerError(Exception):
    """Base exception for compiler errors"""
    pass


class MiniCCompiler:
    """Main compiler class orchestrating all compilation phases"""
    
    def __init__(self, 
                 show_tokens=False, 
                 show_ast=False, 
                 show_ir=False,
                 show_asm=False,
                 optimize_code=True):
        self.show_tokens = show_tokens
        self.show_ast = show_ast
        self.show_ir = show_ir
        self.show_asm = show_asm
        self.optimize_code = optimize_code
    
    def compile(self, source_code: str, source_file: str = "<input>") -> str:
        """
        Compile MiniC source code to C code.
        
        Args:
            source_code: MiniC source code as string
            source_file: Source file name (for error messages)
            
        Returns:
            Generated C code as string
            
        Raises:
            CompilerError: If compilation fails
        """
        try:
            # Phase 1: Lexical Analysis
            print("Phase 1: Lexical Analysis...")
            tokens = lex(source_code)
            
            if self.show_tokens:
                print("\n" + "=" * 70)
                print("TOKENS:")
                print("=" * 70)
                for token in tokens:
                    print(f"  {token}")
                print("=" * 70 + "\n")
            
            # Phase 2: Syntax Analysis (Parsing)
            print("Phase 2: Syntax Analysis (Parsing)...")
            ast = parse(tokens)
            
            if self.show_ast:
                print("\n" + "=" * 70)
                print("ABSTRACT SYNTAX TREE (AST):")
                print("=" * 70)
                print(print_ast(ast))
                print("=" * 70 + "\n")
            
            # Phase 3: Semantic Analysis
            print("Phase 3: Semantic Analysis...")
            analyze(ast)
            
            # Phase 4: Intermediate Code Generation (TAC)
            print("Phase 4: Intermediate Code Generation (TAC)...")
            ir_instructions = generate_ir(ast)
            
            if self.show_ir:
                print("\n" + "=" * 70)
                print("INTERMEDIATE REPRESENTATION (Three-Address Code):")
                print("=" * 70)
                print(print_ir(ir_instructions))
                print("=" * 70 + "\n")
            
            # Phase 5: Optimization
            if self.optimize_code:
                print("Phase 5: Optimization...")
                original_count = len(ir_instructions)
                ir_instructions = optimize(ir_instructions)
                optimized_count = len(ir_instructions)
                
                print(f"  Original instructions: {original_count}")
                print(f"  Optimized instructions: {optimized_count}")
                print(f"  Reduction: {original_count - optimized_count} instructions")
                
                if self.show_ir:
                    print("\n" + "=" * 70)
                    print("OPTIMIZED IR:")
                    print("=" * 70)
                    print(print_ir(ir_instructions))
                    print("=" * 70 + "\n")
            else:
                print("Phase 5: Optimization... (skipped)")
            
            # Phase 6: Code Generation
            print("Phase 6: Code Generation (Assembly)...")
            asm_gen = AssemblyGenerator()
            output_code = asm_gen.generate(ir_instructions)
            
            if self.show_asm:
                print("\n" + "=" * 70)
                print("GENERATED ASSEMBLY CODE:")
                print("=" * 70)
                print(output_code)
                print("=" * 70 + "\n")
            
            print("\n✓ Compilation successful!")
            return output_code
            
        except LexerError as e:
            raise CompilerError(f"Lexical error: {e}")
        except ParseError as e:
            raise CompilerError(f"Parse error: {e}")
        except SemanticError as e:
            raise CompilerError(f"Semantic error: {e}")
        except Exception as e:
            raise CompilerError(f"Compilation error: {e}")


def main():
    """Main entry point for the compiler"""
    parser = argparse.ArgumentParser(
        description='MiniC Compiler - Compile MiniC programs to C',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python minic.py program.mc
  python minic.py program.mc -o program.c
  python minic.py program.mc --show-tokens --show-ast --show-ir
  python minic.py program.mc --no-optimize

For more information, see README.md
        """
    )
    
    parser.add_argument('input', help='Input MiniC source file (.mc)')
    parser.add_argument('-o', '--output', default='output.s',
                       help='Output assembly file (default: output.s)')
    parser.add_argument('--show-tokens', action='store_true',
                       help='Display lexer tokens')
    parser.add_argument('--show-ast', action='store_true',
                       help='Display Abstract Syntax Tree')
    parser.add_argument('--show-ir', action='store_true',
                       help='Display Three-Address Code (IR)')
    parser.add_argument('--show-asm', action='store_true',
                       help='Display generated assembly code')
    parser.add_argument('--no-optimize', action='store_true',
                       help='Disable optimizations')
    
    args = parser.parse_args()
    
    # Check input file exists
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    # Create build directory if it doesn't exist
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # If output is default, put it in build folder with input filename
    if args.output == 'output.s':
        base_name = input_path.stem  # filename without extension
        args.output = str(build_dir / f"{base_name}.s")
    
    # Read source code
    try:
        with open(input_path, 'r') as f:
            source_code = f.read()
    except Exception as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Compile
    print("=" * 70)
    print(f"MiniC Compiler")
    print("=" * 70)
    print(f"Input:  {args.input}")
    print(f"Output: {args.output}")
    print("=" * 70)
    print()
    
    try:
        compiler = MiniCCompiler(
            show_tokens=args.show_tokens,
            show_ast=args.show_ast,
            show_ir=args.show_ir,
            show_asm=args.show_asm,
            optimize_code=not args.no_optimize
        )
        
        output_code = compiler.compile(source_code, str(input_path))
        
        # Write output
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(output_code)
        
        # Suggest binary name in build folder
        binary_name = output_path.stem
        binary_path = build_dir / binary_name
        
        print(f"\n✓ Generated assembly code written to: {args.output}")
        print(f"\nTo assemble and run:")
        print(f"  gcc {args.output} -o {binary_path}")
        print(f"  ./{binary_path}")
        
        return 0
        
    except CompilerError as e:
        print(f"\n✗ Compilation failed!", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error!", file=sys.stderr)
        print(f"{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
