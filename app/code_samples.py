import json


def _build_curl(path: str, method: str, base_url: str, request_body: dict | None, has_api_key: bool) -> str:
    lines = [f'curl -X {method.upper()} "{base_url}{path}"']
    if has_api_key:
        lines.append('  -H "X-API-Key: YOUR_API_KEY"')
    if request_body:
        lines.append('  -H "Content-Type: application/json"')
        body_json = json.dumps(request_body, indent=2)
        lines.append(f"  -d '{body_json}'")
    return " \\\n".join(lines)


def _build_js(path: str, method: str, base_url: str, request_body: dict | None, has_api_key: bool) -> str:
    headers = ['"Content-Type": "application/json"']
    if has_api_key:
        headers.append('"X-API-Key": "YOUR_API_KEY"')
    headers_str = ",\n    ".join(headers)

    body_line = ""
    if request_body:
        body_json = json.dumps(request_body, indent=2)
        indented = "\n".join("  " + line for line in body_json.splitlines())
        body_line = f",\n  body: JSON.stringify({indented.strip()})"

    return f"""const response = await fetch("{base_url}{path}", {{
  method: "{method.upper()}",
  headers: {{
    {headers_str}
  }}{body_line}
}});

const data = await response.json();
console.log(data);"""


def _build_python(path: str, method: str, base_url: str, request_body: dict | None, has_api_key: bool) -> str:
    headers = {}
    if has_api_key:
        headers["X-API-Key"] = "YOUR_API_KEY"

    lines = ["import requests", ""]
    lines.append(f'url = "{base_url}{path}"')
    if headers:
        lines.append(f"headers = {json.dumps(headers, indent=4)}")
    if request_body:
        lines.append(f"payload = {json.dumps(request_body, indent=4)}")

    call_args = []
    if headers:
        call_args.append("headers=headers")
    if request_body:
        call_args.append("json=payload")
    args_str = ", ".join(call_args)

    lines.append(f'response = requests.{method.lower()}(url{", " + args_str if args_str else ""})')
    lines.append("print(response.json())")
    return "\n".join(lines)


def _example_from_schema(schema: dict, components: dict) -> dict | None:
    """Best-effort: pull an `example`/`examples` value, or build a
    minimal example object from property types if none is provided."""
    if not schema:
        return None

    if "$ref" in schema:
        ref_name = schema["$ref"].split("/")[-1]
        schema = components.get("schemas", {}).get(ref_name, {})

    if "example" in schema:
        return schema["example"]

    if schema.get("type") == "object" and "properties" in schema:
        example = {}
        for prop_name, prop_schema in schema["properties"].items():
            if "$ref" in prop_schema:
                example[prop_name] = _example_from_schema(prop_schema, components)
                continue
            prop_type = prop_schema.get("type", "string")
            if "example" in prop_schema:
                example[prop_name] = prop_schema["example"]
            elif prop_type == "string":
                example[prop_name] = prop_schema.get("default", "string")
            elif prop_type == "integer":
                example[prop_name] = prop_schema.get("default", 0)
            elif prop_type == "boolean":
                example[prop_name] = prop_schema.get("default", True)
            elif prop_type == "array":
                example[prop_name] = []
            else:
                example[prop_name] = None
        return example

    return None


def add_code_samples(openapi_schema: dict, base_url: str = "https://caca-authentication.vercel.app") -> dict:
    """Mutates openapi_schema in place, adding x-code-samples to every operation."""
    components = openapi_schema.get("components", {})

    for path, methods in openapi_schema.get("paths", {}).items():
        for method, operation in methods.items():
            if method.lower() not in ("get", "post", "put", "patch", "delete"):
                continue

            # Detect if this endpoint needs an API key header
            has_api_key = any(
                p.get("name") == "X-API-Key" or p.get("name") == "x-api-key"
                for p in operation.get("parameters", [])
            ) or "security" in operation

            # Try to pull a request body example
            request_body = None
            rb = operation.get("requestBody", {})
            content = rb.get("content", {})
            json_content = content.get("application/json", {})
            body_schema = json_content.get("schema", {})
            if body_schema:
                request_body = _example_from_schema(body_schema, components)

            operation["x-code-samples"] = [
                {"lang": "cURL", "source": _build_curl(path, method, base_url, request_body, has_api_key)},
                {"lang": "JavaScript", "source": _build_js(path, method, base_url, request_body, has_api_key)},
                {"lang": "Python", "source": _build_python(path, method, base_url, request_body, has_api_key)},
            ]

    return openapi_schema
