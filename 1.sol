//SPDX-License-Identifier: SimPL-2.0
pragma solidity >0.8.0;
//pragma experimental ABIEncoderV2;


contract dispatch{
    
    address public owner;
    constructor() {
        owner = msg.sender;
    }

    struct User{
        uint id;     //用户id
        string power;    //能源量
        string priority;  //优先级
        string keyword;  //关键字
        string usertime;    //上块时间
        bool sign;      //判断是供电还是需电 true是供电 ，false是需电
        uint index;     //第几轮调度
    }

    struct DispatchTarget{     //调度记录
        uint[] suppliersid;
        uint[] demandersid;
        string dispatchtime; //调度时间
        uint index; //第几轮调度
    }

    uint dispatch_index=0;
    mapping(uint=>User[]) public userinfo;
    //mapping(address=>mapping(uint=>bool)) public purchase_target;
    DispatchTarget[] public dispatchtarget;   //总调度记录
    uint[] resultbyuserid;  //
    uint[] resultbydispatchindex;
    User[] suppliers;
    User[] demanders;
    uint[] suppliersid;
    uint[] demandersid;
    uint supplier_index=0;
    uint demander_index=0;
    User[] resultByuserid;
    function getLength() public view returns(uint){
        return (dispatch_index);
    }

    function addUser(
        uint _id,    //用户id
        string memory _power,    //能源量
        string memory _priority,  //优先级
        string memory _keyword,  //关键字
        string memory _usertime,    //上块时间
        bool _sign      //判断是供电还是需电
    )
    public {    //上传用户信息
        //require(msg.sender == owner,"Only can admin add user info");
        User memory newuser=User(_id,_power,_priority,_keyword,_usertime,_sign,dispatch_index +1);
        if(_sign){
            suppliersid.push(_id);
            supplier_index++;
        }else{
            demandersid.push(_id);
            demander_index++;
        }
        userinfo[_id].push(newuser);
    }


    function addDispatch(
        string memory _dispatchtime    //调度时间
        //uint _index;     //第几轮调度
    )
    public {    //上传调度信息
        //require(msg.sender == owner,"Only can admin dispatch");
        dispatch_index += 1;
        uint[] memory a=copysuppliers(supplier_index);
        uint[] memory b=copydemanders(demander_index);
        DispatchTarget memory _newdispatch=DispatchTarget(a,b,_dispatchtime,dispatch_index);
        dispatchtarget.push(_newdispatch);
    }


    function searchByuserid(uint _id) public returns(User[] memory) {
        for(uint i=0;i<userinfo[_id].length;i++){
            User memory temp1=userinfo[_id][i];
            resultByuserid.push(temp1);
        }
        return resultByuserid;
    }


    function searchBydispatchindex(uint _index) public view returns(uint[] memory,uint[] memory){
        return (dispatchtarget[_index-1].suppliersid,dispatchtarget[_index-1].demandersid);
    }

    function searchByBoth(uint _id,uint _index) public view returns(User memory){
        User memory temp;
        uint length=userinfo[_id].length;
        for(uint i=0;i<length;i++){
            if(userinfo[_id][i].index==_index){
                return userinfo[_id][i];
            }
        }  
        return temp;
    }



    function compareStr (string memory _str1, string memory _str2) public pure returns(bool) {
        if(bytes(_str1).length == bytes(_str2).length){
            if(keccak256(abi.encodePacked(_str1)) == keccak256(abi.encodePacked(_str2))) {
                return true;
            }
        }
        return false;
    }


    function copysuppliers(uint _index) public view returns(uint[] memory){
        uint[] memory b;
        b= new uint[](_index);
        for(uint i=0;i<_index;i++){
            b[i]=suppliers[i].id;
        }
        return b;
    }

    function copydemanders(uint _index) public view returns(uint[] memory){
        uint[] memory b;
        b= new uint[](_index);
        for(uint i=0;i<_index;i++){
            b[i]=demanders[i].id;
        }
        return b;
    }
}