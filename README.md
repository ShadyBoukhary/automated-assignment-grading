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
* Gives the user the option to choose tolerance amount for floating-point numbers
* Gives user the option to ignore student-written descriptions that do not contribute to the solution
* Ignores ASCII table formatting in console apps when needed
* Uses a spellchecker to give leeway on typos in student solutions

### Current Limitations
* Support is exclusive to GitHub
* Only C++ is supported
* Requires executable output to be to the console and not a file
* Does not support assignments that include command-line arguments
* Output with student-made desctiptions forces all strings to be ignored
    * E.g `The number of books is 9` or `number of books: 9` is handled by only comparing numerical values. However, if meaningful strings are also present somewhere else in the key, they will be ignored.
      * Possible solution: enable this feature per line rather than per assignment
* Requires all student output to be consistent
  * Obvious and necessary for all kinds of automated solutions

### Future Work
All limitations are planned to be resolved.
* Support will be extended to all websites that support `Git`
* More languages will be added
* Input and output file support for execuables will be added
  * This could be difficult to implement
* Command-line arguments support will be added
* Multiple-source-file support


