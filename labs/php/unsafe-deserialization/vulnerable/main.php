<?php
// PHP session loader calling unserialize() without restricting allowed classes.
class AdminGadget {
    public string $role = "user";
}
function run(string $raw): string {
    if (str_starts_with($raw, "O:")) {
        $obj = @unserialize($raw);
        if (is_object($obj) && isset($obj->role) && $obj->role === "admin") {
            return "ADMIN_GADGET";
        }
    }
    $data = json_decode($raw, true);
    if (is_array($data) && isset($data["user"]) && is_string($data["user"])) {
        return "USER:" . $data["user"];
    }
    return "DENIED";
}
echo run($argv[1]);
