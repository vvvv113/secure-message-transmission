def jenkins_one_at_a_time_hash(key: str) -> int:
    hash_res = 0
    for i in key:
        hash_res += ord(i)
        hash_res += hash_res << 10
        hash_res ^= hash_res >> 6
    hash_res += (hash_res << 3)
    hash_res ^= (hash_res >> 11)
    hash_res += (hash_res << 15)
    return hash_res
