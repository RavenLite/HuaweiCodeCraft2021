#include <bits/stdc++.h>

#include <utility>

struct Ser_t {
    int core, cpu, tot, day;
};

struct Ser{
    std::string name;
    std::pair<int, int> A, B;
    Ser() = default;
    Ser(std::string _name, const Ser_t& _s) {
        name = std::move(_name);
        A = {_s.core / 2, _s.cpu / 2};
        B = {_s.core / 2, _s.cpu / 2};
    }
};

struct Vir_t {
    int core, cpu, type;
};

struct Vir{
    std::string name;
    int core{}, cpu{}, type{};
    int pos{}, numa{};
    Vir() = default;
    Vir(std::string _name, const Vir_t& _v, int _pos, int _numa) {
        name = std::move(_name);
        core = _v.core;
        cpu = _v.cpu;
        type = _v.type;
        pos = _pos;
        numa = _numa;
    }
};

void runJudger(std::string inputFile,std::string outputFile) {
    std::ifstream infile(inputFile);
    std::ifstream outfile(outputFile);
//    std::cout << "Point1" << std::endl;
//    std::cout << inputFile << std::endl;
//    std::cout << outputFile << std::endl;
    std::string tmp_str;
    int server_type_num;
    infile >> server_type_num;
    infile.ignore();
    // read server type
    std::map<std::string, Ser_t> sts;
    for (int i = 0; i < server_type_num; ++i) {
        infile.ignore();
        getline(infile, tmp_str);
        tmp_str.pop_back();
        std::string name = tmp_str.substr(0, tmp_str.find(','));
        tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
        int core = std::stoi(tmp_str.substr(0, tmp_str.find(',')));
        tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
        int cpu = std::stoi(tmp_str.substr(0, tmp_str.find(',')));
        tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
        int tot = std::stoi(tmp_str.substr(0, tmp_str.find(',')));
        tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
        int day = std::stoi(tmp_str);
        sts[name] = {core, cpu, tot, day};
    }
    int vir_type_num;
    infile >> vir_type_num;
    infile.ignore();
    // read virtual type
    std::map<std::string, Vir_t> vts;
    for (int i = 0; i < vir_type_num; ++i) {
        infile.ignore();
        getline(infile, tmp_str);
        tmp_str.pop_back();
        std::string name = tmp_str.substr(0, tmp_str.find(','));
        tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
        int core = std::stoi(tmp_str.substr(0, tmp_str.find(',')));
        tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
        int cpu = std::stoi(tmp_str.substr(0, tmp_str.find(',')));
        tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
        int type = std::stoi(tmp_str);
        vts[name] = {core, cpu, type};
    }
    int cost = 0, mi = 0;
    std::vector<Ser> sers;
    std::map<int, Vir> virs; // id -> vir
    int T;
    infile >> T;
//    std::cout << "Point2" << std::endl;

    for (int date = 0; date < T; ++date) {
//        std::cout << "Point3" << std::endl;
        auto add_vir_2_ser = [&](const std::string& name, int add_id, int pos, int numa = -1) {
            virs[add_id] = Vir(name, vts[name], pos, numa);
            if (numa == 0) {
                sers[pos].A.first -= virs[add_id].core;
                sers[pos].A.second -= virs[add_id].cpu;
            } else if (numa == 1) {
                sers[pos].B.first -= virs[add_id].core;
                sers[pos].B.second -= virs[add_id].cpu;
            } else {
                sers[pos].A.first -= virs[add_id].core / 2;
                sers[pos].A.second -= virs[add_id].cpu / 2;
                sers[pos].B.first -= virs[add_id].core / 2;
                sers[pos].B.second -= virs[add_id].cpu / 2;
            }
            if (sers[pos].A.first < 0 || sers[pos].A.second < 0 ||
                sers[pos].B.first < 0 || sers[pos].B.second < 0) {
                std::cout << "date " << date << ": add vir " << add_id << " to ser " << pos << " filed\n";
                exit(0);
            }
        };
//        std::cout << "Point4" << std::endl;
        auto del_vir_from_ser = [&](int del_id) {
            if (!virs.count(del_id)) {
                std::cout << "date " << date << ": delete vir " << del_id << " filed\n";
                exit(0);
            }
            if (virs[del_id].type == 0) {
                if (virs[del_id].numa == 0) {
                    sers[virs[del_id].pos].A.first += virs[del_id].core;
                    sers[virs[del_id].pos].A.second += virs[del_id].cpu;
                } else {
                    sers[virs[del_id].pos].B.first += virs[del_id].core;
                    sers[virs[del_id].pos].B.second += virs[del_id].cpu;
                }
            } else {
                sers[virs[del_id].pos].A.first += virs[del_id].core / 2;
                sers[virs[del_id].pos].A.second += virs[del_id].cpu / 2;
                sers[virs[del_id].pos].B.first += virs[del_id].core / 2;
                sers[virs[del_id].pos].B.second += virs[del_id].cpu / 2;
            }
            virs.erase(del_id);
        };
//        std::cout << "Point5" << std::endl;
        // read purchase
        getline(outfile, tmp_str);
        tmp_str.pop_back();
        int buy_num = std::stoi(tmp_str.substr(11));
//        std::cout << "buy_num is :" << buy_num << std::endl;
        for (int i = 0; i < buy_num; ++i) {
            outfile.ignore();
            getline(outfile, tmp_str);
            tmp_str.pop_back();
            std::string name = tmp_str.substr(0, tmp_str.find(','));
            int t_num = std::stoi(tmp_str.substr(tmp_str.find(',') + 2));
//            std::cout << name << " " << t_num << std::endl;
//            std::cout << t_num << std::endl;
//            std::cout << "Point6" << std::endl;
            while (t_num--) {
                if (!sts.count(name)) {
                    std::cout << "date " << date << ": buy server " << name << " filed\n";
                    exit(0);
                }
                sers.emplace_back(name, sts[name]);
                cost += sts[name].tot;
            }
//            std::cout << "Point7" << std::endl;
        }
//        std::cout << "Point8" << std::endl;
        // read migration
        getline(outfile, tmp_str);
        tmp_str.pop_back();
        int mi_num = std::stoi(tmp_str.substr(12));
//        std::cout << "mi_num: " << mi_num << std::endl;
        mi += mi_num;
        if (mi_num > 5 * virs.size() / 1000) {
            std::cerr<<mi_num<<" / "<<virs.size()<<std::endl;
            std::cout << "date " << date << ": migration exceed 5*n/1000\n";
            exit(0);
        }
        for (int i = 0; i < mi_num; ++i) {
            outfile.ignore();
            getline(outfile, tmp_str);
            tmp_str.pop_back();
//            std::cout << "Point9" << std::endl;
            int vir_id = std::stoi(tmp_str.substr(0, tmp_str.find(',')));
            tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
            int pos = std::stoi(tmp_str.substr(0, tmp_str.find(',')));
            tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
            std::string name = virs[vir_id].name;
            int numa = -1;
//            std::cout << "Point10" << std::endl;
//            std::cout << virs[vir_id].type <<std::endl;
            if (virs[vir_id].type == 0) {
//                std::cout << "Point11" << std::endl;
                numa = (int)tmp_str[0] - (int)'A';
//                numa = std::stoi(tmp_str.substr(0, 1));
//                std::cout << numa << std::endl;
//                tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
            }
//            std::cout << "Point11" << std::endl;
            // migration
            del_vir_from_ser(vir_id);
            add_vir_2_ser(name, vir_id, pos, numa);
        }
        // read operator
        int n;
        infile >> n;
        infile.ignore();
        while (n--) {
            infile.ignore();
            getline(infile, tmp_str);
            tmp_str.pop_back();
            if (tmp_str[0] == 'a') {
                tmp_str = tmp_str.substr(5);
                std::string name = tmp_str.substr(0, tmp_str.find(','));
                tmp_str = tmp_str.substr(tmp_str.find(',') + 2);
                int add_id = std::stoi(tmp_str);

                outfile.ignore();
                getline(outfile, tmp_str);
                tmp_str.pop_back();
                if (vts[name].type == 0) {
                    if (tmp_str.back() == 'A') {
                        for (int _ = 0; _ < 3; ++_) tmp_str.pop_back();
                        int pos = std::stoi(tmp_str);
                        add_vir_2_ser(name, add_id, pos, 0);
                    } else {
                        for (int _ = 0; _ < 3; ++_) tmp_str.pop_back();
                        int pos = std::stoi(tmp_str);
                        add_vir_2_ser(name, add_id, pos, 1);
                    }
                } else {
                    int pos = std::stoi(tmp_str);
                    add_vir_2_ser(name, add_id, pos, -1);
                }
            } else {
                tmp_str = tmp_str.substr(5);
                int del_id = std::stoi(tmp_str);
                del_vir_from_ser(del_id);
            }
        }
        // calculate daily-cost
        for (const auto &se : sers) {
            if (se.A.first + se.B.first != sts[se.name].core || se.A.second + se.B.second != sts[se.name].cpu) {
                cost += sts[se.name].day;
            }
        }
    }
    std::cout << "total cost: " << cost << '\n';
    std::cout << "migration num: " << mi << '\n';
}

int main(){
//    std::cout << "Hello world!" << std::endl;
    runJudger("../training_data/training-1.txt","../CloudSchedule-Java/output.txt");
    return 0;
}