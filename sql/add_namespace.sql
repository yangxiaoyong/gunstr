-- 增加iah的namespace

use ftgwebgame;

insert into sys_acl_permissions (namespace, controller, action, aliasname, rbac, in_menu) values
    ('iah', 'statistics', 'index', 'IAH需求统计', 'ACL_NULL', 1);
-- TODO: on dulipcate key where namespace = 'iah' and controller = 'xx'
insert into sys_acl_roles_have_permissions (role_id, permission_id) values (13, 63);

