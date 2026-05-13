def map_lang(lang: str)-> tuple:
    
    lang_map = {
        "python3"    : ".py",
        "python"     : ".py",
        "java"       : ".java",
        "c++"        : ".cpp",
        "c"          : ".c",
        "javascript" : ".js",
        "typescript" : ".ts",
        "golang"     : ".go",
        "rust"       : ".rs",
        "kotlin"     : ".kt",
        "swift"      : ".swift",
        "ruby"       : ".rb",
        "scala"      : ".scala",
        "c#"         : ".cs",
        "php"        : ".php",
    }

    comment_map = {
        ".py"   : "#",
        ".rb"   : "#",
        ".java" : "//",
        ".cpp"  : "//",
        ".c"    : "//",
        ".js"   : "//",
        ".ts"   : "//",
        ".go"   : "//",
        ".rs"   : "//",
        ".kt"   : "//",
        ".cs"   : "//",
        ".php"  : "//",
    }
    lang = lang.lower()
    mapped_lang =lang_map[lang]
    cmnt_map = comment_map[mapped_lang]

    return mapped_lang,cmnt_map