package kubernetes.admission

import future.keywords.contains
import future.keywords.if

# Deny hardcoded secrets in environment variables
deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    env := container.env[_]
    env.value
    contains_secret(env.name)
    msg := sprintf("Container '%s' contains hardcoded secret in env var '%s'. Use secrets instead.", [container.name, env.name])
}

contains_secret(name) if {
    secret_keywords := ["password", "token", "secret", "key", "api_key", "apikey"]
    lower_name := lower(name)
    keyword := secret_keywords[_]
    contains(lower_name, keyword)
}

# Warn about potential sensitive data
warn[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    env := container.env[_]
    env.value
    regex.match("(?i)(pass|pwd|token|secret|key)", env.name)
    msg := sprintf("Container '%s' may contain sensitive data in env var '%s'", [container.name, env.name])
}
