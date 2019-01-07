# AAA

Automated Assignment Assessment (AAA) is an automated system designed for the evaluation of Computer Science based assignments and examinations. AAA makes it incredibly easy for professors or evaluators to grade programming-based assignments.

By simply entering information regarding the students and the assignments, AAA is able to retrieve the assignments from a public repository on the Internet, compile, execute, analyze, and evaluate all individual student assignments. AAA also generates a report describing grade distributions.

### Current Dependencies
AAA requires these to be available in `PATH`:
* Git
* g++

AAA also requires:
* Sudo permissions (to manipulate files in the `home` directory)

### Current Supported Languages
* C++

#### Future Languages
* C
* Java
* Python

### Current Features
* Clone/pull student repositories from GitHub
* Check if source compiles
* Run executable file provided
* Compare line-by-line with a key
* Deduct grades based on weights provided with the key
* Generate Excel Sheet showing grade distribution
* Analyze source code 
    * Verify existence of required functions and methods
    * Check for poor variable names
    * Keep track of loop count

### Current Limitations
* Support is exclusive to GitHub
* Only C++ is supported
* Requires executable output to be to the console and not a file
* Does not support assignments that include command-line arguments
* Executable files must be compatible with the machine running the system
* Student output must match key exactly
  * Could result in inaccurate evalutions for
    * Floating point numbers and precision
    * Output with student-made desctiptions
      * E.g `The number of books is 9` or `number of books: 9`
    * Small typos
  * Requires all student output to be consistent

### Future Work
All limitations are planned to be resolved.
* Support will be extended to all websites that support `Git`
* More languages will be added
* Input and output file support for execuables will be added
  * This could be difficult to implement
* Command-line arguments support will be added
* Cross-platform issues will be resolved by
  * Not requiring executables but relying soley on compiling the code
    * This could be a problem when multiple source files exist
  * Student ouput and key do not have to match 100%
    * Allowing accuracy by a number of decimal points for floating-point numbers will be added
    * Ignoring custom strings like the ones described above that precede the actual results
    * Ignoring output formatting for assignments requiring tables
      * E.g ignoring characters like `-` or `*` when needed

