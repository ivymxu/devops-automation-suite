package kubernetes.admission

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.requests
    msg := sprintf("Container '%s' must define resource requests", [container.name])
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    not container.resources.limits
    msg := sprintf("Container '%s' must define resource limits", [container.name])
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.resources.requests
    not container.resources.requests.memory
    msg := sprintf("Container '%s' must define memory request", [container.name])
}

deny[msg] {
    input.request.kind.kind == "Pod"
    container := input.request.object.spec.containers[_]
    container.resources.requests
    not container.resources.requests.cpu
    msg := sprintf("Container '%s' must define CPU request", [container.name])
}
