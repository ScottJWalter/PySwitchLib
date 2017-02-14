import pyswitch.utilities as util
from pyswitch.os.base.interface import Interface as BaseInterface
from ipaddress import ip_interface

import pyswitch.utilities
import pyswitch.utilities as util
from pyswitch.exceptions import InvalidVlanId


class Interface(BaseInterface):
    """
      The Interface class holds all the actions assocaiated with the Interfaces
      of a NOS device.

      Attributes:
          None
      """

    def __init__(self, callback):
        """
        Interface init function.

        Args:
           callback: Callback function that will be called for each action.

        Returns:
           Interface Object

        Raises:
           None
        """

        super(Interface, self).__init__(callback)

    @property
    def valid_int_types(self):

        return [
            'gigabitethernet',
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet',
            'port_channel'
        ]

    @property
    def valid_intp_types(self):
        return [
            'gigabitethernet',
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet',
        ]

    @property
    def l2_mtu_const(self):
        minimum_mtu = 1522
        maximum_mtu = 9216
        return (minimum_mtu, maximum_mtu)

    @property
    def l3_mtu_const(self):
        minimum_mtu = 1300
        maximum_mtu = 9100
        return (minimum_mtu, maximum_mtu)

    @property
    def l3_ipv6_mtu_const(self):
        minimum_mtu = 1280
        maximum_mtu = 9100
        return (minimum_mtu, maximum_mtu)

    @property
    def has_rbridge_id(self):
        return True

    def fabric_isl(self, **kwargs):
        """Set fabric ISL state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            enabled (bool): Is fabric ISL state enabled? (True, False)
            get (bool): Get config instead of editing config. (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `state` is not specified.
            ValueError: if `int_type`, `name`, or `state` is not a valid value.

        Examples:
            >>> import pyswitch.device
            >>> switches = ['10.24.39.211', '10.24.39.203']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pyswitch.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.fabric_isl(
            ...         int_type='tengigabitethernet',
            ...         name='225/0/40',
            ...         enabled=False)
            ...         dev.interface.fabric_isl()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = str(kwargs.pop('int_type').lower())
        name = str(kwargs.pop('name'))
        enabled = kwargs.pop('enabled', True)
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet'
        ]

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" %
                             repr(int_types))

        if not isinstance(enabled, bool):
            raise ValueError('`enabled` must be `True` or `False`.')

        fabric_isl_args = dict()
        fabric_isl_args[int_type] = name

        if not pyswitch.utilities.valid_interface(int_type, name):
            raise ValueError("`name` must match `^[0-9]{1,3}/[0-9]{1,3}/[0-9]"
                             "{1,3}$`")
        if kwargs.pop('get', False):
            method_name = 'interface_%s_get' % int_type
            config = (method_name, fabric_isl_args)
            op = callback(config, handler='get_config')

            if util.find(op.json, '$..fabric..isl..enable'):
                return True
            return None

        method_name = 'interface_%s_fabric_isl_update' % int_type

        if not enabled:
            fabric_isl_args['fabric_isl_enable'] = False
        else:
            fabric_isl_args['fabric_isl_enable'] = True
        config = (method_name, fabric_isl_args)
        return callback(config)

    def fabric_trunk(self, **kwargs):
        """Set fabric trunk state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, etc)
            name (str): Name of interface. (1/0/5, 1/0/10, etc)
            enabled (bool): Is Fabric trunk enabled? (True, False)
            get (bool): Get config instead of editing config. (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `state` is not specified.
            ValueError: if `int_type`, `name`, or `state` is not a valid value.

        Examples:
            >>> import pyswitch.device
            >>> switches = ['10.24.39.211', '10.24.39.203']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pyswitch.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.fabric_trunk(name='225/0/40',
            ...         int_type='tengigabitethernet', enabled=False)
            ...         dev.interface.fabric_trunk()
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
        """
        int_type = str(kwargs.pop('int_type').lower())
        name = str(kwargs.pop('name'))
        enabled = kwargs.pop('enabled', True)
        callback = kwargs.pop('callback', self._callback)

        int_types = [
            'tengigabitethernet',
            'fortygigabitethernet',
            'hundredgigabitethernet'
        ]

        if int_type not in int_types:
            raise ValueError("`int_type` must be one of: %s" % repr(int_types))

        if not isinstance(enabled, bool):
            raise ValueError('`enabled` must be `True` or `False`.')

        fabric_trunk_args = dict()
        fabric_trunk_args[int_type] = name

        if not pyswitch.utilities.valid_interface(int_type, name):
            raise ValueError("`name` must match `^[0-9]{1,3}/[0-9]{1,3}/[0-9]"
                             "{1,3}$`")

        if kwargs.pop('get', False):
            method_name = 'interface_%s_get' % int_type
            config = (method_name, fabric_trunk_args)
            op = callback(config, handler='get_config')

            if util.find(op.json, '$..fabric..trunk..enable'):
                return True
            return None

        method_name = 'interface_%s_fabric_trunk_update' % int_type

        if not enabled:
            fabric_trunk_args['fabric_trunk_enable'] = False
        else:
            fabric_trunk_args['fabric_trunk_enable'] = True
        config = (method_name, fabric_trunk_args)
        return callback(config)

    def ip_anycast_gateway(self, **kwargs):
        """
        Add anycast gateway under interface ve.

        Args:
            int_type: L3 interface type on which the anycast ip
               needs to be configured.
            name:L3 interface name on which the anycast ip
               needs to be configured.
            anycast_ip: Anycast ip which the L3 interface
               needs to be associated.
            enable (bool): If ip anycast gateway should be enabled
                or disabled.Default:``True``.
            get (bool) : Get config instead of editing config. (True, False)
            rbridge_id (str): rbridge-id for device. Only required when type is
                `ve`.
            callback (function): A function executed upon completion of the
               method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.
        Returns:
            Return value of `callback`.
        Raises:
            KeyError: if `int_type`, `name`, `anycast_ip` is not passed.
            ValueError: if `int_type`, `name`, `anycast_ip` is invalid.
        Examples:
            >>> import pyswitch.device
            >>> switches = ['10.24.39.211', '10.24.39.203']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pyswitch.device.Device(conn=conn, auth=auth) as dev:
            ...         output = dev.interface.ip_anycast_gateway(
            ...         int_type='ve',
            ...         name='89',
            ...         anycast_ip='10.20.1.1/24',
            ...         rbridge_id='1')
            ...         output = dev.interface.ip_anycast_gateway(
            ...         get=True,int_type='ve',
            ...         name='89',
            ...         anycast_ip='10.20.1.1/24',
            ...         rbridge_id='1')
            ...         output = dev.interface.ip_anycast_gateway(
            ...         enable=False,int_type='ve',
            ...         name='89',
            ...         anycast_ip='10.20.1.1/24',
            ...         rbridge_id='1')
            ...         # doctest: +IGNORE_EXCEPTION_DETAIL
            Traceback (most recent call last):
            KeyError
         """

        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        anycast_ip = kwargs.pop('anycast_ip', '')
        enable = kwargs.pop('enable', True)
        get = kwargs.pop('get', False)
        rbridge_id = kwargs.pop('rbridge_id', '1')
        callback = kwargs.pop('callback', self._callback)
        valid_int_types = ['ve']

        if get and anycast_ip == '':
            enable = None
            if int_type not in valid_int_types:
                raise ValueError('`int_type` must be one of: %s' %
                                 repr(valid_int_types))
            anycast_args = dict(ve=name)

            method_name1 = 'rbridge_id_interface_%s_ip_anycast_address_get' % int_type
            method_name2 = 'rbridge_id_interface_%s_ipv6_anycast_address_get' % int_type
            anycast_args['rbridge_id'] = rbridge_id
            if not pyswitch.utilities.valid_vlan_id(name):
                raise InvalidVlanId("`name` must be between `1` and `8191`")

            config1 = (method_name1, anycast_args)
            config2 = (method_name2, anycast_args)
            result = []
            op = callback(config1, handler='get_config')
            result.append(util.find(op.json, '$..ip-address'))
            op = callback(config2, handler='get_config')
            result.append(util.find(op.json, '$..ipv6-address'))

            return result

        ipaddress = ip_interface(unicode(anycast_ip))
        if int_type not in valid_int_types:
            raise ValueError('`int_type` must be one of: %s' %
                             repr(valid_int_types))
        if anycast_ip != '':
            ipaddress = ip_interface(unicode(anycast_ip))
            if ipaddress.version == 4:
                anycast_args = dict(
                    ve=name, ip_anycast_address=(str(anycast_ip),))
                method_name = 'rbridge_id_interface_%s_ip_anycast_address' % int_type
            elif ipaddress.version == 6:
                anycast_args = dict(
                    ve=name, ipv6_anycast_address=(
                        str(anycast_ip),))
                method_name = 'rbridge_id_interface_%s_ipv6_anycast_address' % int_type

        anycast_args['rbridge_id'] = rbridge_id

        if not pyswitch.utilities.valid_vlan_id(name):
            raise InvalidVlanId("`name` must be between `1` and `8191`")
        create_method = "%s_create" % method_name
        config = (create_method, anycast_args)
        print config

        if not enable:
            delete_method = "%s_delete" % method_name
            config = (delete_method, anycast_args)
        return callback(config)

    def spanning_tree_state(self, **kwargs):
        """Set Spanning Tree state.

        Args:
            int_type (str): Type of interface. (gigabitethernet,
                tengigabitethernet, vlan, port_channel etc).
            name (str): Name of interface or VLAN id.
                (For interface: 1/0/5, 1/0/10 etc).
                (For VLANs 0, 1, 100 etc).
                (For Port Channels 1, 100 etc).
            enabled (bool): Is Spanning Tree enabled? (True, False)
            callback (function): A function executed upon completion of the
                method.  The only parameter passed to `callback` will be the
                ``ElementTree`` `config`.

        Returns:
            Return value of `callback`.

        Raises:
            KeyError: if `int_type`, `name`, or `enabled` is not passed.
            ValueError: if `int_type`, `name`, or `enabled` are invalid.

        Examples:
            >>> import pyswitch.device
            >>> switches = ['10.24.39.211', '10.24.39.203']
            >>> auth = ('admin', 'password')
            >>> for switch in switches:
            ...     conn = (switch, '22')
            ...     with pyswitch.device.Device(conn=conn, auth=auth) as dev:
            ...         enabled = True
            ...         int_type = 'tengigabitethernet'
            ...         name = '225/0/37'
            ...         output = dev.interface.enable_switchport(int_type,
            ...         name)
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         enabled = False
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         int_type = 'vlan'
            ...         name = '102'
            ...         enabled = False
            ...         output = dev.interface.add_vlan_int(name)
            ...         output = dev.interface.enable_switchport(
            ...             int_type, name)
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         enabled = False
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         output = dev.interface.del_vlan_int(name)
            ...         int_type = 'port_channel'
            ...         name = '2'
            ...         enabled = False
            ...         output = dev.interface.channel_group(name='225/0/20',
            ...                              int_type='tengigabitethernet',
            ...                              port_int=name,
            ...                              channel_type='standard',
            ...                              mode='active')
            ...         output = dev.interface.enable_switchport(
            ...             int_type, name)
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         enabled = False
            ...         output = dev.interface.spanning_tree_state(
            ...         int_type=int_type, name=name, enabled=enabled)
            ...         output = dev.interface.remove_port_channel(
            ...             port_int=name)
        """
        int_type = kwargs.pop('int_type').lower()
        name = kwargs.pop('name')
        get = kwargs.pop('get', False)

        callback = kwargs.pop('callback', self._callback)
        valid_int_types = self.valid_int_types
        valid_int_types.append('vlan')

        if int_type not in valid_int_types:
            raise ValueError('int_type must be one of: %s' %
                             repr(valid_int_types))
        state_args = dict()
        state_args[int_type] = name
        if get:
            method_name = 'interface_%s_get' % int_type
            if int_type == 'vlan':
                method_name = 'vlan_get'
            config = (method_name, state_args)
            x = callback(config, handler='get_config')

            if util.find(x.json, '$..spanning-tree..shutdown'):
                return False
            return True

        enabled = kwargs.pop('enabled')
        if not isinstance(enabled, bool):
            raise ValueError('%s must be `True` or `False`.' % repr(enabled))

        if int_type == 'vlan':
            if not pyswitch.utilities.valid_vlan_id(name):
                raise InvalidVlanId('%s must be between 0 to 8191.' % int_type)
            shutdown_name = 'stp_shutdown'
            method_name = 'interface_%s_spanning_tree_update' % int_type

        else:
            if not pyswitch.utilities.valid_interface(int_type, name):
                raise ValueError('`name` must be in the format of x/y/z for '
                                 'physical interfaces or x for port channel.')
            shutdown_name = 'shutdown'
            method_name = 'interface_%s_spanning_tree_update' % int_type

        if enabled:
            state_args[shutdown_name] = False
        else:
            state_args[shutdown_name] = True
        try:
            config = (method_name, state_args)
            return callback(config)
        # TODO: Catch existing 'no shut'
        # This is in place because if the interface spanning tree is already
        # up,`ncclient` will raise an error if you try to admin up the
        # interface again.
        # TODO: add logic to shutdown STP at protocol level too.
        except AttributeError:
            return None
